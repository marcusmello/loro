# pylint: skip-file

from typing import List, Optional

from pydantic import BaseModel, validator

MESSAGES_DIRECTIONS = [
    "incoming",
    "outcoming",
]


class Choice(BaseModel):
    text: str
    leads_to: str = str()  # Answer tag


class Answer(BaseModel):
    tag: str
    header: str
    choices: Optional[List[Choice]]

    def choices_indexes_list(self):
        return [(self.choices.index(c) + 1) for c in self.choices]

    def formatted_text(self, invalid_choice_header: str = str()) -> str:
        choice = "*{}* - {}\n"
        choices_text = "".join(
            [
                choice.format((self.choices.index(c) + 1), c.text)
                for c in self.choices
            ]
        )

        return "{}\n\n{}\n\n{}\n".format(
            invalid_choice_header, self.header, choices_text
        )


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


EMPTY_ANSWER = Answer(
    tag=str(),
    header=str(),
    choices=list(),
)
