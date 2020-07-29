from starlette.config import Config
from starlette.middleware.sessions import Secret

import databases

config = Config(env_file=".env")

DATABASE_URL = config("DATABASE_URL", cast=databases.DatabaseURL)
SESSION_SECRET_KEY = config("SESSION_SECRET_KEY", cast=Secret)
REGISTRATION_ENABLED = config("REGISTRATION_ENABLED", cast=bool, default=False)

OAUTH_BASE_URL = config("OAUTH_BASE_URL")

GITHUB_CLIENT_ID = config("GITHUB_CLIENT_ID", default=None)
GITHUB_CLIENT_SECRET = config("GITHUB_CLIENT_SECRET", cast=Secret, default=None)
