# pylint: skip-file

import sys
from typing import Union

from environs import Env
from pydantic import BaseModel, BaseSettings

thismodule = sys.modules[__name__]
env = Env()


class TwilioParameters(BaseModel):
    auth_token = env.str(
        "TWILIO_AUTH_TOKEN", default="no_token"
    )
    callback_hook_path = "/twilio-hook"


class Timesettings(BaseModel):
    local_timezone = env.str("LOCAL_TIMEZONE", default="America/Bahia")
    system_timezone = env.str("SYSTEM_TIMEZONE", default="UTC")
    default_timestamp_unit = env.str("DEFAULT_TIMESTAMP_UNIT", default="s")
    human_readable_format = env.str(
        "HUMAN_READABLE_FORMAT", default="YYYY-MM-DD HH:mm:ss"
    )
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
    update_error: str = str()
    delete: str = str()

    def generate(self):
        self.create = "{}/create".format(self.root)
        self.create_error = "{}/create-error".format(self.root)
        self.read = self.root
        self.update = "{}/update".format(self.root)
        self.update_error = "{}/update-error".format(self.root)
        self.delete = "{}/delete".format(self.root)


answers_paths = RestPath(root="/answers")
answers_paths.generate()


class UrlPaths(BaseModel):
    answers = answers_paths


class CorsOrigins(BaseModel):
    paths: dict = UrlPaths().dict()
    protocols: list = ["http", "https"]
    main_domain: str = "localhost"
    main_port: int = 8000

    domains: list = (
        ",{},".format(main_domain).join(["127.0.0.1", "0.0.0.0"])
    ).split(",")

    ports: list = (",{},".format(main_port).join(["80", "443"])).split(",")

    def generate(self):
        all_paths = []
        all_paths = [
            r[1]
            for r in [route.items() for route in self.paths.values()][0]
            if r[1] not in all_paths
        ]
        simple_urls = [
            "{}://{}{}".format(protocol, domain, path)
            for protocol in self.protocols
            for domain in self.domains
            for path in all_paths
        ]
        port_urls = [
            "{}://{}:{}{}".format(protocol, domain, port, path)
            for protocol in self.protocols
            for domain in self.domains
            for port in self.ports
            for path in all_paths
        ]

        return simple_urls + port_urls


class AnswersDynamicFormVariables(BaseModel):
    default_empty_tag: str = "Tag Seguinte"


class WebTemplatingVariables(BaseModel):
    answers_dynamic_forms = AnswersDynamicFormVariables()


def possible_variation(string: str):
    return [
        string,
        string.capitalize(),
        string.upper(),
        string.lower(),
        string.swapcase(),
        string.casefold(),
    ]


class DefaultChoices(BaseModel):
    show: bool = True
    common_header: str = """... ou digite:\n\n"""
    invalid_common_header: str = "*Escolha inválida*"
    back_base_word: str = "voltar"
    exit_base_word: str = "sair"

    back_words_list: list = possible_variation(string=back_base_word)
    exit_words_list: list = possible_variation(string=exit_base_word)
    
    back_choice_text:str = (
        """*{}* - retornar ao menu anterior\n""".format(back_base_word)
    )
    exit_choice_text:str = """*{}* - encerrar o atendimento\n""".format(
        exit_base_word
    )


class WellcomeAnswer(BaseModel):
    tag = "welcome"
    header = env.str("WELCOME_ANSWER_HEADER", default="env-fail")

class ExitAnswer(BaseModel):
    tag = "exit"
    header = "Atendimento finalizado, obrigado!"

class Settings(BaseSettings):
    class Config:
        arbitrary_types_allowed = True

    relational_database: BaseModel = get_relational_database(
        provider=env.str("RELATIONAL_DATABASE_PROVIDER", default="sqlite")
    )
    sql_debug: bool = False
    API_prefix_version: str = "/api/v1"
    url_paths = UrlPaths()
    web_templating_variables = WebTemplatingVariables()
    cors_origins = CorsOrigins()
    default_choices = DefaultChoices()
    wellcome_answer = WellcomeAnswer()
    exit_answer = ExitAnswer()
    twilio = TwilioParameters()


settings = Settings()
