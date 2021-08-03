# pylint:disable=missing-module-docstring
# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=too-few-public-methods
# pylint:disable=no-name-in-module

import sys
from typing import List
from pydantic import BaseModel

from app.lib.utils.schemas import Answer, Choice
from app.lib.utils.tools.string_conversion import case_variations


thismodule = sys.modules[__name__]

WELCOME_TAG = "abertura"
EXIT_TAG = "saída"
SERVICE_1_TAG = "servico1"
SERVICE_2_TAG = "servico2"

LINK_1_1_TAG = "link1.1"
LINK_1_2_TAG = "link1.2"
LINK_1_3_TAG = "link1.3"

LINK_2_1_TAG = "link2.1"
LINK_2_2_TAG = "link2.2"


def fake_link(tag: str):
    return "www.lororesolve.fake/{}".format(tag.split(sep="link")[1])


FAKE_SERVICE_1 = Answer(
    tag=SERVICE_1_TAG,
    header="Você escolheu o *PRIMEIRO* serviço. Qual a categoria desejada?",
    choices=[
        Choice(
            text="Categoria 1",
            leads_to=LINK_1_1_TAG,
        ),
        Choice(
            text="Categoria 2",
            leads_to=LINK_1_2_TAG,
        ),
        Choice(
            text="Categoria 3",
            leads_to=LINK_1_3_TAG,
        ),
    ],
)

FAKE_SERVICE_2 = Answer(
    tag=SERVICE_2_TAG,
    header="Você escolheu o *SEGUNDO* serviço. Qual a categoria desejada?",
    choices=[
        Choice(
            text="Categoria 1",
            leads_to=LINK_2_1_TAG,
        ),
        Choice(
            text="Categoria 2",
            leads_to=LINK_2_2_TAG,
        ),
    ],
)


def fake_answers_factory() -> List[Choice]:
    services = [1, 2]
    categories = [1, 2, 3]

    answers = [FAKE_SERVICE_1, FAKE_SERVICE_2]
    for service in services:
        for category in categories:
            try:
                tag = getattr(
                    thismodule, "LINK_{}_{}_TAG".format(service, category)
                )
                answers.append(
                    Answer(
                        tag=tag,
                        header="Resolvido! Basta clicar no link abaixo\
                            para resolver o serviço *{}* categoria\
                            *{}*:\n\n{}".format(
                            service, category, fake_link(tag)
                        ),
                        choices=list(),
                    )
                )
            except AttributeError:
                pass
    return answers


class DefaultAnswers(BaseModel):

    welcome_answer: Answer = Answer(
        tag=WELCOME_TAG,
        header="Olá, eu sou o Lôro, seu atendente virtual",
        choices=[
            Choice(text="Proseguir para o serviço 1", leads_to=SERVICE_1_TAG),
            Choice(text="Proseguir para o serviço 2", leads_to=SERVICE_2_TAG),
        ],
    )
    exit_answer: Answer = Answer(
        tag=EXIT_TAG, header="Atendimento finalizado, obrigado!", choices=[]
    )
    extra: List[Answer] = fake_answers_factory()


class DefaultChoices(BaseModel):
    show: bool = True
    common_header: str = """... ou digite:\n\n"""
    invalid_common_header: str = "*Escolha inválida*"
    back_base_word: str = "voltar"
    exit_base_word: str = "sair"

    back_words_list: list = case_variations(string=back_base_word)
    exit_words_list: list = case_variations(string=exit_base_word)

    back_choice_text: str = """*{}* - retornar ao menu anterior\n""".format(
        back_base_word
    )
    exit_choice_text: str = """*{}* - encerrar o atendimento\n""".format(
        exit_base_word
    )
