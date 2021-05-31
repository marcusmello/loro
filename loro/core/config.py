# pylint: skip-file

import sys
from typing import Union

from environs import Env
from pydantic import BaseModel, BaseSettings

thismodule = sys.modules[__name__]
env = Env()


class Timesettings(BaseModel):
    local_timezone = env.str("LOCAL_TIMEZONE", default="America/Bahia")
    system_timezone = env.str("SYSTEM_TIMEZONE", default="UTC")
    default_timestamp_unit = "s"
    human_readable_format = "YYYY-MM-DD HH:mm:ss"
    presented_in_human_readable_format = True


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


class RestPath(BaseModel):
    root: str
    create: str = str()
    create_error = str()
    read: str = str()
    update: str = str()
    delete: str = str()

    def generate(self):
        self.create = "{}/create".format(self.root)
        self.create_error = "{}/create-error".format(self.root)
        self.read = self.root
        self.update = "{}/update/".format(self.root)
        self.delete = self.root


dialogs_paths = RestPath(root="/dialogs")
dialogs_paths.generate()


class UrlPaths(BaseModel):
    dialogs = dialogs_paths


class DialogsDynamicFormVariables(BaseModel):
    default_empty_tag: str = "Tag Seguinte"


class WebTemplatingVariables(BaseModel):
    dialogs_dynamic_forms = DialogsDynamicFormVariables()


class Settings(BaseSettings):
    class Config:
        arbitrary_types_allowed = True

    API_V1_STR: str = "/api/v1"
    relational_database: BaseModel = get_relational_database(
        provider=env.str("RELATIONAL_DATABASE_PROVIDER", default="sqlite")
    )
    sql_debug: bool = False
    url_paths = UrlPaths()
    web_templating_variables = WebTemplatingVariables()


settings = Settings()
