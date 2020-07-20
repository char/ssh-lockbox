import bcrypt

from starlette.requests import Request
from starlette.responses import RedirectResponse

from ssh_key_authority.db import database, users
from ssh_key_authority.flashes import flash


async def login_valid(username, password):
    query = users.select().where(users.c.username == username)
    matching_user = await database.fetch_one(query=query)
    if matching_user:
        user_id, user_username, user_password_hash = matching_user

        return bcrypt.checkpw(
            password.encode("utf-8"), user_password_hash.encode("ascii")
        )

    return False


async def login_endpoint(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    if (username and password) and await login_valid(username, password):
        request.session["username"] = username
        flash(request, "success", "Logged in.")
    else:
        flash(
            request,
            "error",
            "The username and password specified not match a user. Please try again.",
        )

    return RedirectResponse("/", 303)


async def logout_endpoint(request: Request):
    del request.session["username"]
    flash(request, "success", "Logged out.")
    return RedirectResponse("/", 303)
