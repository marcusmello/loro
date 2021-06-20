from typing import List

from fastapi import APIRouter, HTTPException, Form
from loro.lib.utils import schemas
from loro.lib.utils.db.sql.crud import answers

router = APIRouter()


@router.post("/", response_model=schemas.Answer)
def create_answer(answer: schemas.Answer):
    answer_in_db = answers.read(tag=answer.tag)
    if answer_in_db:
        raise HTTPException(
            status_code=400, detail="Tag já existe, defina outra."
        )

    return answers.create(answer)


@router.get("/{tag}", response_model=schemas.Answer)
def read_answer(tag: str):
    answer_in_db = answers.read(tag=tag)
    if not answer_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return answer_in_db


@router.put("/{tag}", response_model=schemas.Answer)
def update_answer(tag: str, new_answer: schemas.Answer):
    answer_in_db = answers.read(tag=tag)
    if not answer_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return answers.update(tag=tag, new_answer=new_answer)


@router.delete("/{tag}")
def delete(tag: str):
    answer_in_db = answers.read(tag=tag)
    if not answer_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return answers.delete(tag=tag)


@router.get("/", response_model=List[schemas.Answer])
def get_answers(limit: int = 100):
    return answers.get_collection(limit=limit)
