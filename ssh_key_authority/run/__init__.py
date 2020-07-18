from ssh_key_authority import routes, middleware
from starlette.applications import Starlette

app = Starlette(routes=routes, middleware=middleware)
