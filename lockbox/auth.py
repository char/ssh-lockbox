from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser
from starlette.requests import Request


class SessionAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        if (username := request.session.get("username")) :
            return AuthCredentials(["authenticated"]), SimpleUser(username)
