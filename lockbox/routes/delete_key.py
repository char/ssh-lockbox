from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.background import BackgroundTask

from lockbox.flashes import flash
from lockbox.db import users, keys, database
from lockbox.integrations import run_key_delete_integrations


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

    background_task = None

    async with database.transaction():
        flash(request, "success", "Deleted key.")

        query = (
            keys.select()
            .where(keys.c.user_id == user_id)
            .where(keys.c.key_comment == key_comment)
        )
        key = await database.fetch_one(query)

        ssh_algo, ssh_contents, ssh_comment = key[2:]

        query = (
            keys.delete()
            .where(keys.c.user_id == user_id)
            .where(keys.c.key_comment == key_comment)
        )
        await database.execute(query)

        background_task = BackgroundTask(
            run_key_delete_integrations, user_id, ssh_algo, ssh_contents, ssh_comment
        )

    return RedirectResponse("/", 303, background=background_task)
