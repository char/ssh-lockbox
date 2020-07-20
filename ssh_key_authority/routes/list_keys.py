from typing import Generator

from starlette.requests import Request
from starlette.responses import PlainTextResponse

from ssh_key_authority.db import database, keys, users


def generate_key_info(ssh_keys, include_comments: bool) -> Generator[str, None, None]:
    for ssh_key in ssh_keys:
        key_id, user_id, key_algo, key_contents, key_comment = ssh_key
        yield (
            f"{key_algo} {key_contents} {key_comment}"
            if include_comments
            else f"{key_algo} {key_contents}"
        )


async def list_keys_endpoint(request: Request):
    """Serve a list of keys for a user.
    
    We include the comment fields if and only if authentication is provided.
    """

    query = users.select().where(users.c.username == request.path_params["user"])
    user = await database.fetch_one(query)
    if not user:
        return PlainTextResponse("User does not exist.", 404)

    query = keys.select().where(keys.c.user_id == user[0])
    ssh_keys = await database.fetch_all(query)

    include_comments = False  # TODO: Match an Authorization header value
    return PlainTextResponse("\n".join(generate_key_info(ssh_keys, include_comments)))
