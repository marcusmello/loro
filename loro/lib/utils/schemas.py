# pylint: skip-file

from typing import List, Optional

from pydantic import BaseModel, validator

MESSAGES_DIRECTIONS = [
    "incoming",
    "outcoming",
]


class Choice(BaseModel):
    text: str
    leads_to: str = str() # Interaction (Dialog or Return) tag


class Return(BaseModel):
    tag: str
    content: str


class Dialog(BaseModel):
    tag: str
    header: str
    choices: Optional[List[Choice]]
    leads_to: str = str() # Interaction (Dialog or Return) tag


class Message(BaseModel):
    content: str
    direction: str
    timestamp: int

    @validator("direction")
    def direction_must_exist(cls, value):
        if value not in MESSAGES_DIRECTIONS:
            raise ValueError("invalid direction")
        return value


class FinalClient(BaseModel):
    id: int
    messages: List[Message]
