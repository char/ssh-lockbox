from starlette.requests import Request

from lockbox.db import database, users, keys
from lockbox.templating import render_template
from lockbox.config import REGISTRATION_ENABLED


async def main_page_endpoint(request: Request):
    """Render the main page. Shows either a login form or an SSH key submission form"""

    context = {"registration_enabled": REGISTRATION_ENABLED}

    if request.user.is_authenticated:
        query = users.select().where(users.c.username == request.user.username)
        user = await database.fetch_one(query)
        assert user is not None

        query = keys.select().where(keys.c.user_id == user[0])
        user_ssh_keys = await database.fetch_all(query)
        user_ssh_keys = [(key[2], key[3], key[4]) for key in user_ssh_keys]

        context["user_ssh_keys"] = user_ssh_keys

    return render_template(request, "index.html.j2", **context)
