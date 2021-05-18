#pylint:disable=missing-module-docstring
# pylint:disable=too-few-public-methods
# pylint:disable=missing-class-docstring

from environs import Env
from pydantic import BaseSettings

env = Env()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    domain = env.str("DOMAIN", default="http://127.0.0.1:8000")


settings = Settings()
