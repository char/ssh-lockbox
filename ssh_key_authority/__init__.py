from starlette.routing import Route, Mount
from starlette.config import Config
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from os.path import realpath

templates = Jinja2Templates(directory="templates")


async def index_page(request):
    return templates.TemplateResponse("index.html.j2", {"request": request})


async def login(req):
    # TODO: Sign in a user by username and password, and set a session cookie.
    # Always redirect to the main page; if login fails, we can show a flash to the user.
    pass


async def create_key_entry(req):
    # TODO: Parse the request form and create a key entry for the authenticated user.
    # Authentication should be possible via Bearer token or session cookies.
    pass


async def fetch_keys(req):
    # user = req.path_params["user"]
    # TODO: Return a text/plain response containing this user's SSH keys.
    # If a valid authentication token is provided, include the SSH keys' comment fields.
    pass


routes = [
    Route("/", endpoint=index_page),
    Route("/login", endpoint=login),
    Route("/create", endpoint=create_key_entry, methods=["POST"]),
    Route("/keys/{user}", endpoint=fetch_keys),
    Mount(
        "/static",
        app=StaticFiles(
            directory=realpath("static")
        ),  # FIXME: Starlette 0.13.5 has a bug that forces us to realpath() the static directory
        name="static",
    ),
]

middleware = []
