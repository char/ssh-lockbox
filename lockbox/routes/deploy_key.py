from typing import Tuple, Optional

from starlette.requests import Request
from starlette.responses import RedirectResponse

from lockbox.flashes import flash
from lockbox.db import database, keys, users


class InvalidKeyException(Exception):
    """Invalid key - something is wrong with the key."""


def parse_ssh_key(plaintext_key: str) -> Tuple[str, str, Optional[str]]:
    key_parts = plaintext_key.split(None, 2)
    if len(key_parts) < 2:
        raise InvalidKeyException(
            "Unexpected key format: type and base64 encoded public key data is required"
        )

    comment = None
    if len(key_parts) == 3:
        comment = key_parts[2]

    return key_parts[0], key_parts[1], comment


async def deploy_key_endpoint(request: Request):
    if not request.user.is_authenticated:
        flash(request, "error", "Cannot deploy key: You are not logged in.")
        return RedirectResponse("/", 303)

    form_data = await request.form()

    plaintext_key = form_data.get("key")
    if not plaintext_key:
        flash(request, "error", "'key' is a required field.")
        return RedirectResponse("/", 303)
    plaintext_key = plaintext_key.strip()

    try:
        ssh_algo, ssh_contents, ssh_comment = parse_ssh_key(plaintext_key)
        async with database.transaction():
            query = users.select().where(users.c.username == request.user.username)
            user_id = await database.fetch_val(query)

            query = keys.insert().values(
                user_id=user_id,
                key_algorithm=ssh_algo,
                key_contents=ssh_contents,
                key_comment=ssh_comment,
            )
            await database.execute(query)

            flash(request, "success", "The provided SSH key has been deployed.")
            # TODO: Dispatch background tasks for GitHub, Gitea, etc
    except:
        flash(request, "error", "Invalid key data.")

    return RedirectResponse("/", 303)
