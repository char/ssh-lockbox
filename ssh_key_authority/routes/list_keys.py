from typing import Generator

from starlette.requests import Request
from starlette.responses import PlainTextResponse

from ssh_key_authority.db import database, keys, users, access_keys


def generate_key_info(ssh_keys, include_comments: bool) -> Generator[str, None, None]:
    for ssh_key in ssh_keys:
        key_id, user_id, key_algo, key_contents, key_comment = ssh_key
        yield (
            f"{key_algo} {key_contents} {key_comment}"
            if include_comments
            else f"{key_algo} {key_contents}"
        )


async def access_key_matches(user_id):
    query = access_keys.select().where(access_keys.c.user_id == user_id)
    async for row in database.iterate(query):
        access_key_token = row[3]

        if auth_header_parts[1] == access_key_token:
            return True

    return False


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

    include_comments = request.user.username == user[1]

    if (authorization_header := request.headers.get("Authorization")) :
        auth_header_parts = authorization_header.split()
        if len(auth_header_parts) > 1 and auth_header_parts[0].casefold() == "bearer":
            if await access_key_matches(user[0], auth_header_parts[1]):
                include_comments = True

    return PlainTextResponse("\n".join(generate_key_info(ssh_keys, include_comments)))
