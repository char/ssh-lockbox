from typing import List, Set

from urllib.parse import urlencode
import httpx

import json
import asyncio

from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse
from starlette.background import BackgroundTask

from lockbox.config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, OAUTH_BASE_URL
from lockbox.db import database, users, user_integrations, keys
from lockbox.flashes import flash

from lockbox.integrations import ThirdPartyIntegration, get_integration_from_db

GITHUB_INTEGRATION_TYPE = "GitHub"

GITHUB_REDIRECT_URL = OAUTH_BASE_URL + "/integrations/github/complete"


def github_integration_enabled():
    return bool(GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET)


async def initiate_github_integration(request: Request):
    if not github_integration_enabled():
        return PlainTextResponse("GitHub integration is currently disabled.")

    if not request.user.is_authenticated:
        flash(request, "error", "You are not logged in!")
        return RedirectResponse("/", 303)

    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URL,
        "scope": "admin:public_key",
    }

    return RedirectResponse(
        "https://github.com/login/oauth/authorize?" + urlencode(params)
    )


async def complete_github_integration(request: Request):
    if not github_integration_enabled():
        return PlainTextResponse("GitHub integration is currently disabled.")

    if not request.user.is_authenticated:
        flash(request, "error", "You are not logged in!")
        return RedirectResponse("/")

    code = request.query_params.get("code")
    if not code:
        flash(request, "error", "Invalid OAuth code")
        return RedirectResponse("/")

    query = users.select().where(users.c.username == request.user.username)
    user_id = await database.fetch_val(query)

    async with httpx.AsyncClient() as http:
        res = await http.post(
            "https://github.com/login/oauth/access_token",
            params={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": str(GITHUB_CLIENT_SECRET),
                "code": code,
            },
            headers={"Accept": "application/json"},
        )

        if res.is_error or "error" in res.json():  # Why is this a 2xx, GitHub?
            print("Could not complete GitHub OAuth:")
            print(res.json())
            flash(
                request,
                "error",
                "An error occurred while trying to authenticate with GitHub",
            )
            return RedirectResponse("/")

        async with database.transaction():
            query = user_integrations.insert().values(
                user_id=user_id,
                integration_type=GITHUB_INTEGRATION_TYPE,
                integration_domain="github.com",
                integration_data=res.json(),  # { "access_token": ..., "token_type": ... }
            )
            await database.execute(query)

            query = (  # Why does encode.io's databases module make it so hard to get back the created record?
                user_integrations.select()
                .where(user_integrations.c.user_id == user_id)
                .where(user_integrations.c.integration_type == GITHUB_INTEGRATION_TYPE)
                .where(user_integrations.c.integration_domain == "github.com")
            )
            user_integration_row = await database.fetch_one(query)

            flash(request, "success", "Added GitHub integration for 'github.com'")

        async with get_integration_from_db(user_integration_row) as integration:
            return RedirectResponse(
                "/", background=BackgroundTask(integration.full_sync)
            )


async def force_sync_github_integration(request):
    """Force sync any GitHub integrations for this user (via POST request only)"""

    if not request.user.is_authenticated:
        flash(request, "error", "You are not logged in!")
        return RedirectResponse("/", 303)

    username = request.user.username
    query = users.select().where(users.c.username == request.user.username)
    user_id = await database.fetch_val(query)

    query = (
        user_integrations.select()
        .where(user_integrations.c.user_id == user_id)
        .where(user_integrations.c.integration_type == GITHUB_INTEGRATION_TYPE)
    )

    integrations = await database.fetch_all(query)
    for integration_row in integrations:
        async with get_integration_from_db(integration_row) as integration:
            await integration.full_sync()

    return PlainTextResponse("Success.")


def _create_authed_http(access_token) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        headers={
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }
    )


class GitHubIntegration(ThirdPartyIntegration):
    def __init__(self, user_id, integration_domain, integration_data):
        super().__init__(user_id, integration_domain, integration_data)
        self.http = _create_authed_http(integration_data["access_token"])

    async def aclose(self):
        await self.http.aclose()

    async def _iter_keys(self):
        domain = self.integration_domain
        res = await self.http.get(
            f"https://api.{domain}/user/keys", params={"per_page": 100}
        )

        for existing_key in res.json():
            yield existing_key

        while next_url := res.links.get("next"):
            res = await self.http.get(next_url)
            for existing_key in res.json():
                yield existing_key

    async def full_sync(self):
        ssh_keys = await database.fetch_all(
            keys.select().where(keys.c.user_id == self.user_id)
        )

        existing_keys = set()
        async for key in self._iter_keys():
            existing_keys.add(key["key"])

        coroutines = []
        for ssh_key in ssh_keys:
            key_algorithm, key_contents, key_comment = ssh_key[2:]
            if f"{key_algorithm} {key_contents}" in existing_keys:
                continue

            coroutines.append(
                self._deploy_key(key_algorithm, key_contents, key_comment)
            )

        await asyncio.gather(*coroutines)

    async def on_new_key(self, key_algorithm, key_contents, key_comment):
        domain = self.integration_domain
        response = await self.http.post(
            f"https://api.{domain}/user/keys",
            json={
                "title": key_comment,
                "key": f"{key_algorithm} {key_contents} {key_comment}",
            },
        )

        if response.is_error:
            print("Error while deploying key to GitHub:")
            print(response.json())

    async def on_delete_key(self, key_algorithm, key_contents, key_comment):
        domain = self.integration_domain

        async for key in self._iter_keys():
            if key["key"] == f"{key_algorithm} {key_contents}":
                key_id = key["id"]

                response = await self.http.delete(
                    f"https://api.{domain}/user/keys/{key_id}"
                )

                if response.is_error:
                    print("Error while deleting key from GitHub:")
                    print(response.json())
