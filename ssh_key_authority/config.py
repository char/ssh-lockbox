from starlette.config import Config
from starlette.middleware.sessions import Secret

import databases

config = Config(env_file=".env")

DATABASE_URL = config("DATABASE_URL", cast=databases.DatabaseURL)
SESSION_SECRET_KEY = config("SESSION_SECRET_KEY", cast=Secret)
REGISTRATION_ENABLED = config("REGISTRATION_ENABLED", cast=bool, default=False)
# TODO: INVITES_ENABLED ?
