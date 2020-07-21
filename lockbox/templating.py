from starlette.requests import Request
from starlette.templating import Jinja2Templates

from lockbox.flashes import get_and_clear_flashes

templates = Jinja2Templates(directory="templates")


def render_template(request: Request, template_name: str, **kwargs):
    context = {"request": request, "flashes": get_and_clear_flashes(request)}
    context.update(kwargs)
    return templates.TemplateResponse(template_name, context)
