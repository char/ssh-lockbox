from starlette.requests import Request

from ssh_key_authority import templates
from ssh_key_authority.config import REGISTRATION_ENABLED


async def main_page_endpoint(request: Request):
    return templates.TemplateResponse(
        "index.html.j2",
        {"request": request, "registration_enabled": REGISTRATION_ENABLED},
    )
