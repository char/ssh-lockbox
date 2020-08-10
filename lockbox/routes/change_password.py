import bcrypt

from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse

from lockbox.templating import render_template
from lockbox.db import database, users
from lockbox.config import REGISTRATION_ENABLED
from lockbox.flashes import flash


async def change_password_page_endpoint(request: Request):
    """Render the change password form"""

    if not request.user.is_authenticated:
        flash(request, "error", "You are not logged in.")
        return RedirectResponse("/", 303)

    return render_template(request, "change_password.html.j2")


async def change_password_endpoint(request: Request):
    """Process a change password form submission (via POST request only)"""

    if not request.user.is_authenticated:
        flash(request, "error", "You are not logged in.")
        return RedirectResponse("/", 303)

    query = users.select().where(users.c.username == request.user.username)
    user = await database.fetch_one(query=query)
    user_id, user_username, user_password_hash = user.values()

    form_data = await request.form()
    current_password = form_data.get("current_password")
    password = form_data.get("password")
    password_confirm = form_data.get("password_confirm")

    has_errors = False

    if not current_password:
        has_errors = True
        flash(request, "error", "'current_password' is a required field.")

    if not password:
        has_errors = True
        flash(request, "error", "'password' is a required field.")

    if not password_confirm:
        has_errors = True
        flash(request, "error", "'password_confirm' is a required field.")

    if not bcrypt.checkpw(
        current_password.encode("utf-8"), user_password_hash.encode("ascii")
    ):
        has_errors = True
        flash(request, "error", "The provided password confirmation is incorrect.")

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

    if has_errors:
        return RedirectResponse("/change_password/", 303)

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    password_hash = password_hash.decode("ascii")

    async with database.transaction():
        update_query = (
            users.update()
            .where(users.c.username == request.user.username)
            .values(password_hash=password_hash)
        )

        await database.execute(update_query)

        flash(request, "success", "Password changed.")

    return RedirectResponse("/", 303)
