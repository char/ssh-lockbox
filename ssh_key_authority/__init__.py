from starlette.applications import Starlette
from starlette.routing import Route, Mount

from starlette.requests import Request

from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from starlette.staticfiles import StaticFiles

from ssh_key_authority.db import database
from ssh_key_authority.config import SESSION_SECRET_KEY
from ssh_key_authority.auth import SessionAuthBackend

from ssh_key_authority.routes.main_page import main_page_endpoint
from ssh_key_authority.routes.login import login_endpoint, logout_endpoint
from ssh_key_authority.routes.register import register_page_endpoint, register_endpoint
from ssh_key_authority.routes.deploy_key import deploy_key_endpoint
from ssh_key_authority.routes.list_keys import list_keys_endpoint

app = Starlette(
    routes=[
        Route("/", endpoint=main_page_endpoint),
        Route("/login", endpoint=login_endpoint, methods=["POST"]),
        Route("/logout", endpoint=logout_endpoint, methods=["POST"]),
        Route("/register/", endpoint=register_page_endpoint),
        Route("/register", endpoint=register_endpoint, methods=["POST"]),
        Route("/deploy", endpoint=deploy_key_endpoint, methods=["POST"]),
        Route("/keys/{user}", endpoint=list_keys_endpoint),
        Mount("/static", app=StaticFiles(directory="static"), name="static",),
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY),
        Middleware(AuthenticationMiddleware, backend=SessionAuthBackend()),
    ],
    on_startup=[database.connect],
    on_shutdown=[database.disconnect],
)
