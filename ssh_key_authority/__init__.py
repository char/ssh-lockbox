from starlette.applications import Starlette
from starlette.routing import Route, Mount

from starlette.requests import Request

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from starlette.staticfiles import StaticFiles
from os.path import realpath


async def fetch_keys(request):
    # user = request.path_params["user"]
    # TODO: Return a text/plain response containing this user's SSH keys.
    # If valid authentication is present, include the SSH keys' comment fields.
    pass


from ssh_key_authority.db import database
from ssh_key_authority.config import SESSION_SECRET_KEY
from ssh_key_authority.auth import SessionAuthBackend

from ssh_key_authority.routes.main_page import main_page_endpoint
from ssh_key_authority.routes.login import login_endpoint, logout_endpoint
from ssh_key_authority.routes.register import register_page_endpoint, register_endpoint
from ssh_key_authority.routes.deploy_key import deploy_key_endpoint

app = Starlette(
    routes=[
        Route("/", endpoint=main_page_endpoint),
        Route("/login", endpoint=login_endpoint, methods=["POST"]),
        Route("/logout", endpoint=logout_endpoint, methods=["POST"]),
        Route("/register/", endpoint=register_page_endpoint),
        Route("/register", endpoint=register_endpoint, methods=["POST"]),
        Route("/deploy", endpoint=deploy_key_endpoint, methods=["POST"]),
        Route("/keys/{user}", endpoint=fetch_keys),
        Mount(
            "/static",
            app=StaticFiles(
                directory=realpath("static")
            ),  # FIXME: Starlette 0.13.5 has a bug that forces us to realpath() the static directory
            name="static",
        ),
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY),
        Middleware(AuthenticationMiddleware, backend=SessionAuthBackend()),
    ],
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
