#from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

settings = Settings()
