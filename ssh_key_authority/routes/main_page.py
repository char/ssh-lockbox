from starlette.requests import Request

from ssh_key_authority.templating import render_template
from ssh_key_authority.config import REGISTRATION_ENABLED


async def main_page_endpoint(request: Request):
    """Render the main page. Shows either a login form or an SSH key submission form"""
    return render_template(
        request, "index.html.j2", registration_enabled=REGISTRATION_ENABLED
    )
