# pylint:disable=missing-module-docstring
# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=too-few-public-methods
# pylint:disable=no-name-in-module

from pydantic import BaseModel

class AnswersDynamicFormVariables(BaseModel):
    default_empty_tag: str = "Tag Seguinte"


class WebTemplatingVariables(BaseModel):
    answers_dynamic_forms = AnswersDynamicFormVariables()
