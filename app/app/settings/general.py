# pylint:disable=missing-module-docstring
# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=too-few-public-methods
# pylint:disable=no-name-in-module

from environs import Env
from pydantic import BaseModel, BaseSettings

from .default_answers import (
    DefaultChoices,
    DefaultAnswers,
)

from .database_adapters import get_relational_database
from .url_paths_handler import UrlPaths, CorsOrigins
from .web_templating import WebTemplatingVariables

env = Env()


class TwilioParameters(BaseModel):
    auth_token = env.str("TWILIO_AUTH_TOKEN", default="no_token")
    callback_hook_path = env.str(
        "TWILIO_CALLBACK_HOOK_PATH", default="/twilio-hook"
    )


class Timesettings(BaseModel):
    local_timezone = env.str("LOCAL_TIMEZONE", default="America/Bahia")
    system_timezone = env.str("SYSTEM_TIMEZONE", default="UTC")
    default_timestamp_unit = env.str("DEFAULT_TIMESTAMP_UNIT", default="s")
    human_readable_format = env.str(
        "HUMAN_READABLE_FORMAT", default="YYYY-MM-DD HH:mm:ss"
    )
    present_as_human_readable = env.bool(
        "PRESENT_AS_HUMAN_READABLE", default=True
    )


class DefaultSettings(BaseSettings):
    class Config:
        arbitrary_types_allowed = True

    sql_debug: bool = env.bool("SQL_DEBBUG", default=False)
    create_extra_answers_on_startup: bool = env.bool(
        "CREATE_EXTRA_ANSWERS_ON_STARTUP", default=True
    )
    show_default_choices: bool = env.bool("SHOW_DEFAULT_CHOICES", default=True)

    API_prefix_version: str = env.str("API_PREFIX_VERSION", default="/api/v1")

    relational_database: BaseModel = get_relational_database(
        provider=env.str("RELATIONAL_DATABASE_PROVIDER", default="sqlite")
    )

    default_answers = DefaultAnswers()
    default_choices = DefaultChoices()

    url_paths = UrlPaths()
    web_templating_variables = WebTemplatingVariables()
    cors_origins = CorsOrigins()

    twilio = TwilioParameters()


settings = DefaultSettings()
