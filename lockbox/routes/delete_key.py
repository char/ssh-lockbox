from starlette.requests import Request
from starlette.responses import RedirectResponse

from lockbox.flashes import flash
from lockbox.db import users, keys, database


async def delete_key_endpoint(request: Request):
    """Delete a key for the logged in user via its comment"""
    if not request.user.is_authenticated:
        flash(request, "error", "You are not logged in!")
        return RedirectResponse("/", 303)

    form_data = await request.form()
    key_comment = form_data.get("key_comment")
    if not key_comment:
        flash(request, "error", "key_comment is a required field.")
        return RedirectResponse("/", 303)

    query = users.select().where(users.c.username == request.user.username)
    user_id = await database.fetch_val(query)

    async with database.transaction():
        query = (
            keys.delete()
            .where(keys.c.user_id == user_id)
            .where(keys.c.key_comment == key_comment)
        )
        await database.execute(query)
        flash(request, "success", "Deleted key.")

    return RedirectResponse("/", 303)
