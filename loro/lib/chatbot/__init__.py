import json

from loro.core.config import settings
from loro.lib.utils import schemas
from loro.lib.utils.db.sql.crud import answers
from pydantic import BaseModel


WELLCOME_TAG = settings.wellcome.tag


def create_wellcome_answer_if_it_not_exists():
    wellcome_answer = answers.read(tag=WELLCOME_TAG)
    if not wellcome_answer:
        wellcome_answer = schemas.Answer(
            tag=WELLCOME_TAG, header=settings.wellcome.header, choices=list()
        )
        answers.create(answer=wellcome_answer)


class AnswerSequence:
    def __init__(self, string: str):
        self.string: string
        self.separator = "!&$"

    def transform_into_list(self):
        if not self.string:
            return [WELLCOME_TAG]

        answers_sequence_raw_list = self.string.split(sep=self.separator)
        return [tag for tag in answers_sequence_raw_list if tag.strip()]

    def make_string(self, answer_sequence_list: list):
        self.string = self.separator.join(answer_sequence_list)

    def flush(self):
        self.string = str()


class ChatFlowHandler:
    def __init__(self, from_user: str, form):
        self.answer_sequence = None
        self.answer_sequence_list = None
        self.from_ = from_user
        self.form = form
        self.current_answer = schemas.EMPTY_ANSWER
        self.next_answer = schemas.EMPTY_ANSWER
        self.response = str()

    def _wellcome_proceed(self):
        pass

    def _make_response(self, answer: schemas.Answer):
        return answer.formatted_text()

    def exit_chat(self):
        self.answer_sequence.flush()

    def back_chat(self):
        self.answer_sequence_list = self.answer_sequence_list[:-1]
        self.response = self._make_response(
            answer=answers.read(tag=self.answer_sequence_list[-1])
        )
        self.answer_sequence.make_string(
            answer_sequence_list=self.answer_sequence_list
        )

    def invalid_choice(self):
        invalid_msg = "Escolha inválida."
        self.response = "{}\n{}".format(
            invalid_msg, self._make_response(answer=self.current_answer)
        )

    def _proceed_user_choice(self, choice: str):

        if choice in settings.default_choices.exit_choices:
            return self.exit_chat()

        if choice in settings.default_choices.back_choices:
            return self.back_chat()

        try:
            choice = int(choice)
        except:
            choice = 99999999

        return choice

    def run(self, incoming_msg: str, answer_sequence_string: str):
        self.answer_sequence = AnswerSequence(string=answer_sequence_string)
        self.answer_sequence_list = self.answer_sequence.transform_into_list()

        if not answer_sequence_string:
            return self._wellcome_proceed()

        return self._proceed_user_choice(choice=incoming_msg.strip())
