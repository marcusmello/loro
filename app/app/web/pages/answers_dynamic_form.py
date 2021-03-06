# pylint: skip-file

from app.settings.general import settings
from app.lib.utils import schemas
from app.lib.utils.db.sql.crud.answers import get_all_tags
from pydantic import BaseModel

from .router import Request

paths = settings.url_paths.answers
templating_vars = settings.web_templating_variables.answers_dynamic_forms

DEFAULT_EMPTY_TAG = templating_vars.default_empty_tag


class AlreadyFilledChoicesMenu(BaseModel):
    html: str = str()
    index: int = 1


class FormDescriptor(BaseModel):
    is_valid: bool
    form_class: str


class ValidForm(BaseModel):
    is_valid = True
    form_class = "form-control"


class InvalidForm(BaseModel):
    is_valid = False
    form_class = "form-control is-invalid"


class FormControl(BaseModel):
    valid: FormDescriptor = ValidForm()
    invalid: FormDescriptor = InvalidForm()


def choice_text_input(default=str()) -> str:
    return """
        <td>
            <input type="text" name="choiceText"
            id="choiceText" placeholder="Texto da opção"
            class="form-control name_list" value="{}"/>
        </td>
        """.format(
        default
    )


def tag_selector(selected_tag=DEFAULT_EMPTY_TAG) -> str:
    # Look at https://getbootstrap.com/docs/5.0/forms/form-control/#datalists
    selector_template = """
        <td>
            <select class="form-control" name="choiceTag" 
            id="choiceTag" aria-label="Default select example">
                <option selected>{}</option>
                {}
            </select>
        </td>
        """
    tags = get_all_tags()
    if selected_tag in tags:
        tags.remove(selected_tag)

    option_template = """<option value="{}">{}</option>\n"""
    options = "".join([option_template.format(tag, tag) for tag in tags])

    return selector_template.format(selected_tag, options)


def remove_button(index: int) -> str:
    return """
            <td>
                <button type="button" name="remove" id="{}" 
                class="btn btn-danger btn_remove">
                    <span class="fa fa-trash" 
                    data-toggle="tooltip" title="Excluir"></span>
                </button>
            </td>
        </tr>
        """.format(
        index
    )


class CommonContext(BaseModel):
    originTag: str = str()
    blockTitle: str = "Novo"
    update = False
    choicesAlreadyFilled: str = str()
    dynamicFieldStartIndex: int = 1
    postURL: str = paths.create
    successReturnURL: str = paths.root
    errorReturnURL: str = paths.create_error
    answer: schemas.Answer = schemas.EMPTY_ANSWER
    formControl: FormDescriptor = ValidForm()
    choiceTextInput: str = choice_text_input()
    choiceTagSelector: str = str()
    welcome_tag:str = settings.default_answers.welcome_answer.tag
    exit_tag: str = settings.default_answers.exit_answer.tag

    def refresh_tag_selector(self):
        tag_selector_ = tag_selector()
        self.choiceTagSelector = tag_selector_


class ParseForm:
    @staticmethod
    def check_tag(tag: str) -> str:
        if tag == DEFAULT_EMPTY_TAG:
            return str()
        return tag

    def _list_to_schema(self, form: list) -> schemas.Answer:
        tag = form.pop(0)
        header = form.pop(0)

        choices = list()
        while form:
            choice = schemas.Choice(
                text=form.pop(0), leads_to=self.check_tag(tag=form.pop(0))
            )
            if choice.text:
                choices.append(choice)

        return schemas.Answer(tag=tag, header=header, choices=choices)

    def from_raw_form(self, answer_form: list) -> schemas.Answer:
        return self._list_to_schema(form=[item[1] for item in answer_form])

    def from_raw_invalid_input(self, data: list) -> schemas.Answer:
        data_list = data.split(sep="&")
        return self._list_to_schema(
            form=[item.split(sep="=")[1] for item in data_list]
        )


class DynamicContext:
    @staticmethod
    def _filled(choice: schemas.Choice, index: int) -> str:
        choice_text = choice_text_input(default=choice.text)
        choice_tag_selector = tag_selector(
            selected_tag=(
                DEFAULT_EMPTY_TAG
                if choice.leads_to == str()
                else choice.leads_to
            )
        )

        return """<tr id="row{}" class="dynamic-added">\n{}\n{}\n{}""".format(
            index,
            choice_text,
            choice_tag_selector,
            remove_button(index),
        )

    def _already_filled(self, choices: list) -> AlreadyFilledChoicesMenu:
        if not choices:
            return AlreadyFilledChoicesMenu()

        filled_choices = [
            self._filled(choice, index=choices.index(choice) + 1)
            for choice in choices
        ]

        return AlreadyFilledChoicesMenu(
            html="".join(filled_choices), index=len(filled_choices) + 1
        )

    @staticmethod
    def _common_context():
        context = CommonContext()
        context.refresh_tag_selector()
        return context

    def default_create(self, request: Request) -> dict:
        context = self._common_context()
        return {**context.dict(), **dict(request=request)}

    def _filled_context(self, answer: schemas.Answer) -> CommonContext:
        already_filled_choices = self._already_filled(choices=answer.choices)
        context = self._common_context()

        context.choicesAlreadyFilled = already_filled_choices.html
        context.dynamicFieldStartIndex = already_filled_choices.index
        context.answer = answer

        return context

    def invalid_create(self, request: Request, answer: schemas.Answer) -> dict:
        context = self._filled_context(answer)
        context.formControl = InvalidForm()
        return {**context.dict(), **dict(request=request)}

    def _update_context(
        self, tag: str, answer: schemas.Answer
    ) -> CommonContext:
        context = self._filled_context(answer)
        context.blockTitle = "Atualizar"
        context.update = True
        context.postURL = paths.update + "/{}/".format(tag)
        context.errorReturnURL = paths.update_error + "/{}".format(tag)
        context.originTag = tag
        return context

    def default_update(
        self, request: Request, tag: str, answer: schemas.Answer
    ) -> dict:

        context = self._update_context(tag, answer)
        return {**context.dict(), **dict(request=request)}

    def invalid_update(
        self, request: Request, tag: str, answer: schemas.Answer
    ) -> dict:

        context = self._update_context(tag, answer)
        context.formControl = InvalidForm()
        return {**context.dict(), **dict(request=request)}
