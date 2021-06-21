import json
from typing import List, Union
from app.lib.utils import schemas
from app.lib.utils.db.sql.models import Answer
from pony.orm import db_session, select


def answer_schema(answer: Answer) -> schemas.Answer:
    return schemas.Answer(
        tag=answer.tag,
        header=answer.header,
        choices=[
            schemas.Choice(**(json.loads(choice))) for choice in answer.choices
        ],
    )


def answer_dict(answer: schemas.Answer) -> dict:
    return dict(
        tag=answer.tag,
        header=answer.header,
        choices=[choice.json() for choice in answer.choices],
    )


@db_session
def create(answer: schemas.Answer) -> schemas.Answer:
    answer_to_db = Answer(**answer_dict(answer))
    return answer_schema(answer_to_db)


@db_session
def read(tag: str) -> schemas.Answer:
    try:
        return answer_schema(Answer.get(tag=tag))
    except (KeyError, AttributeError):
        return None


@db_session
def update(tag: str, new_answer: schemas.Answer) -> schemas.Answer:
    answer_in_db = Answer.get(tag=tag)
    answer_in_db.update(**answer_dict(new_answer))

    return answer_schema(answer_in_db)


@db_session
def delete(tag: str) -> dict:
    answer_in_db = Answer.get(tag=tag)
    answer_in_db.delete()
    return dict(delete="ok")


@db_session
def get_collection(limit: int) -> List[Union[dict, schemas.Answer]]:
    try:
        answers = Answer.select().order_by((Answer.tag))[:limit]
        return [answer_schema(answer) for answer in answers]
    except:
        return [dict()]

@db_session
def get_all_tags() -> List[str]:
    try:
        return list(select(answer.tag for answer in Answer))
    except:
        return list()