import bcrypt

from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse

from ssh_key_authority.templating import render_template
from ssh_key_authority.db import database, users
from ssh_key_authority.config import REGISTRATION_ENABLED
from ssh_key_authority.flashes import flash


async def disabled_registration_endpoint(request: Request):
    """Return a plain text response for when registration is disabled.

    This is used for both endpoints: the page at /register/ and the form action at /register.
    """
    return PlainTextResponse("Registration is currently disabled.")


async def real_register_page_endpoint(request: Request):
    """Render the registration form"""
    if request.user.is_authenticated:
        return RedirectResponse("/", 303)

    return render_template(request, "register.html.j2")


async def user_already_exists(username: str) -> bool:
    query = users.select(users.c.username == username)
    return (await database.fetch_one(query)) is not None


async def real_register_endpoint(request: Request):
    """Process a registration form submission (via POST request only)"""
    form_data = await request.form()

    username = form_data.get("username")
    password = form_data.get("password")
    password_confirm = form_data.get("password_confirm")

    has_errors = False

    if await user_already_exists(username):
        has_errors = True
        flash(request, "error", "This username is already taken!")

    if len(password) < 32:
        has_errors = True
        flash(
            request,
            "error",
            "The provided password is too short. It must be at least 32 characters in length.",
        )

    if password != password_confirm:
        has_errors = True
        flash(
            request,
            "error",
            "The provided password does not match the password confirmation.",
        )

    if not has_errors:
        flash(request, "success", "Successfully registered. Please log in.")
        async with database.transaction():
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("ascii")
            query = users.insert().values(
                username=username, password_hash=password_hash
            )
            await database.execute(query)

    return RedirectResponse("/register/" if has_errors else "/", 303)


register_page_endpoint = (
    real_register_page_endpoint
    if REGISTRATION_ENABLED
    else disabled_registration_endpoint
)

register_endpoint = (
    real_register_endpoint if REGISTRATION_ENABLED else disabled_registration_endpoint
)
