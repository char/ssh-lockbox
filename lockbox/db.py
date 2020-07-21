from lockbox.config import DATABASE_URL

import databases
import sqlalchemy

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("password_hash", sqlalchemy.String, nullable=False),
)

keys = sqlalchemy.Table(
    "keys",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    ),
    sqlalchemy.Column("key_algorithm", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("key_contents", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("key_comment", sqlalchemy.String, nullable=False),
)

access_keys = sqlalchemy.Table(
    "access_keys",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    ),
    sqlalchemy.Column("access_key_description", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("access_key_token", sqlalchemy.String, nullable=False),
)
