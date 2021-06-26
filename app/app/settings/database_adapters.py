# pylint:disable=missing-module-docstring
# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=too-few-public-methods
# pylint:disable=no-name-in-module

import sys
from typing import Union

from environs import Env
from pydantic import BaseModel

thismodule = sys.modules[__name__]
env = Env()


class PostgresDatabase(BaseModel):
    provider: str = "postgres"
    host: str = env.str("DB_HOST", default="localhost")
    port: int = env.int("POSTGRES_PORT", default=5432)
    database: str = env.str("POSTGRES_DB", default="postgres_db")
    user: str = env.str("POSTGRES_USER", default="postgres_user")
    password: str = env.str(
        "POSTGRES_PASSWORD", default="123_postgres_password"
    )


class SqliteDatabase(BaseModel):
    provider: str = "sqlite"
    filename: str = "database.sqlite"
    create_db: bool = True


class MemorySqliteDatabase(BaseModel):
    provider: str = "sqlite"
    filename: str = ":memory:"


def get_relational_database(
    provider: str,
) -> Union[PostgresDatabase, SqliteDatabase]:

    return getattr(thismodule, "{}Database".format(provider.capitalize()))()
