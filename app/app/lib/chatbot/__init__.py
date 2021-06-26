import json

from app.lib.utils import schemas
from app.lib.utils.db.sql.crud import answers
from app.settings.general import settings
from pydantic import BaseModel

DEFAULT_ANSWERS = settings.default_answers
WELCOME_TAG = DEFAULT_ANSWERS.welcome_answer.tag
EXIT_TAG = settings.default_answers.exit_answer.tag
DEFAULT_CHOICES = settings.default_choices


class DefaultAnswers:
    @staticmethod
    def create_if_do_not_exist(answer: schemas.Answer):
        answer_in_db = answers.read(tag=answer.tag)
        if not answer_in_db:
            answers.create(answer=answer)

    def create(self):
        self.create_if_do_not_exist(answer=DEFAULT_ANSWERS.welcome_answer)
        self.create_if_do_not_exist(answer=DEFAULT_ANSWERS.exit_answer)

        if settings.create_extra_answers_on_startup:
            for answer in DEFAULT_ANSWERS.extra:
                self.create_if_do_not_exist(answer=answer)


class AnswerSequence:
    def __init__(self, string: str):
        self.string_ = string
        self.separator_ = "!&$"
        self.list_ = list()

    def make_list(self):
        if not self.string_:
            self.list_ = [WELCOME_TAG]
            return None

        answers_sequence_raw_list = self.string_.split(sep=self.separator_)
        self.list_ = [tag for tag in answers_sequence_raw_list if tag.strip()]
        return None

    def make_string(self):
        self.string_ = self.separator_.join(self.list_)

    def flush(self):
        self.string_ = str()
        self.list_ = list()


class ChatFlowHandler:
    def __init__(self, from_user: str, form):
        self.answer_sequence = None
        self.from_ = from_user
        self.form = form
        self.current_answer = schemas.EMPTY_ANSWER
        self.response = str()

    def render_response(self, choice_not_valid=False, final_answer=False):
        sub_header = str()
        extra_default_choices_text = "{}{}".format(
            DEFAULT_CHOICES.common_header, DEFAULT_CHOICES.exit_choice_text
        )

        if choice_not_valid:
            sub_header = DEFAULT_CHOICES.invalid_common_header

        if self.current_answer.tag != WELCOME_TAG:
            extra_default_choices_text += DEFAULT_CHOICES.back_choice_text

        response = self.current_answer.formatted_text(sub_header)

        if (
            DEFAULT_CHOICES.show
            and self.current_answer.tag != EXIT_TAG
            and not final_answer
        ):
            response += extra_default_choices_text

        if final_answer:
            exit_answer = answers.read(tag=EXIT_TAG)
            response += exit_answer.formatted_text()

        self.response = response

    def first_wellcome_proceed(self):
        self.answer_sequence.make_string()

        self.current_answer = answers.read(tag=WELCOME_TAG)
        self.render_response()

    def exit_chat(self):
        self.answer_sequence.flush()

        self.current_answer = answers.read(tag=EXIT_TAG)
        self.render_response()

    def back_chat(self):
        self.answer_sequence.list_.pop()
        self.answer_sequence.make_string()

        current_answer_tag = self.answer_sequence.list_[-1]
        self.current_answer = answers.read(tag=current_answer_tag)
        self.render_response()

    @staticmethod
    def _pass_choice_to_integer(choice: str) -> int:
        try:
            return int(choice)
        except ValueError:
            return 99999999

    def _valid_choice(self, choice: int):
        next_answer_tag = (self.current_answer.choices[choice - 1]).leads_to
        self.answer_sequence.list_.append(next_answer_tag)
        self.answer_sequence.make_string()

        self.current_answer = answers.read(tag=next_answer_tag)
        self.render_response()

        if not self.current_answer.choices_indexes_list():
            self.answer_sequence.flush()
            self.render_response(final_answer=True)

    def _invalid_choice(self):
        self.answer_sequence.make_string()
        self.render_response(choice_not_valid=True)

    def _choice_selector(self, choice: str):
        if choice in DEFAULT_CHOICES.exit_words_list:
            return self.exit_chat()

        if (
            choice in DEFAULT_CHOICES.back_words_list
            and self.current_answer.tag != WELCOME_TAG
        ):
            return self.back_chat()

        if not self.current_answer.choices_indexes_list():
            self.answer_sequence.flush()
            self.render_response(final_answer=True)
            return None

        integer_choice = self._pass_choice_to_integer(choice=choice)

        if integer_choice in self.current_answer.choices_indexes_list():
            return self._valid_choice(choice=integer_choice)

        return self._invalid_choice()

    def run(self, incoming_msg: str, answer_sequence_string: str):
        self.answer_sequence = AnswerSequence(string=answer_sequence_string)
        self.answer_sequence.make_list()

        if not answer_sequence_string:
            return self.first_wellcome_proceed()

        current_answer_tag = self.answer_sequence.list_[-1]
        self.current_answer = answers.read(tag=current_answer_tag)
        return self._choice_selector(choice=incoming_msg.strip())
