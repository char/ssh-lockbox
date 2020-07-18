from starlette.config import Config
import databases

config = Config(env_file=".env")
DATABASE_URL = config("DATABASE_URL", cast=databases.DatabaseURL)
