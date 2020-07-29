from typing import Optional

from lockbox.db import database, user_integrations

# TODO: What logic can we re-use from the GitHub integration for other services?


class ThirdPartyIntegration:
    def __init__(self, user_id: int, integration_domain: str, integration_data: dict):
        self.user_id = user_id
        self.integration_domain = integration_domain
        self.integration_data = integration_data

    async def aclose(self):
        pass

    async def full_sync(self):
        raise NotImplementedError(
            f"'full_sync' is not implemented for {self.__class__.__name__}"
        )

    async def on_new_key(self, key_algorithm, key_contents, key_comment):
        raise NotImplementedError(
            f"'on_new_key' is not implemented for {self.__class__.__name__}"
        )

    async def on_delete_key(self, key_algorithm, key_contents, key_comment):
        raise NotImplementedError(
            f"'on_delete_key' is not implemented for {self.__class__.__name__}"
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type=None, exc_value=None, traceback=None):
        await self.aclose()


integrations = {}


def get_integration_from_db(user_integration_row):
    (
        user_id,
        integration_type,
        integration_domain,
        integration_data,
    ) = user_integration_row[1:]

    integration_class = integrations.get(integration_type)
    if not integration_class:
        return None

    return integration_class(user_id, integration_domain, integration_data)


async def get_integrations_for_user(user_id: int):
    query = user_integrations.select().where(user_integrations.c.user_id == user_id)
    async for user_integration in database.iterate(query):
        async with get_integration_from_db(user_integration) as integration:
            yield integration


async def run_key_deploy_integrations(
    user_id: int, key_algorithm: str, key_contents: str, key_comment: str
):
    async for integration in get_integrations_for_user(user_id):
        await integration.on_new_key(key_algorithm, key_contents, key_comment)


async def run_key_delete_integrations(
    user_id: int, key_algorithm: str, key_contents: str, key_comment: str
):
    async for integration in get_integrations_for_user(user_id):
        await integration.on_delete_key(key_algorithm, key_contents, key_comment)


from lockbox.integrations.github import GitHubIntegration

integrations["GitHub"] = GitHubIntegration
