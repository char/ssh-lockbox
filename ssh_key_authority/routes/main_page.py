from starlette.requests import Request

from ssh_key_authority import templates
from ssh_key_authority.config import REGISTRATION_ENABLED
from ssh_key_authority.flashes import get_and_clear_flashes


async def main_page_endpoint(request: Request):
    """Render the main page. Shows either a login form or an SSH key submission form"""
    return templates.TemplateResponse(
        "index.html.j2",
        {
            "request": request,
            "flashes": get_and_clear_flashes(request),
            "registration_enabled": REGISTRATION_ENABLED,
        },
    )
