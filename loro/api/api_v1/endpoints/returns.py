from typing import List

from fastapi import APIRouter, HTTPException, Form
from loro.lib.utils import schemas
from loro.lib.utils.db.sql.crud import returns

router = APIRouter()


@router.post("/", response_model=schemas.Return)
def create(tag: str = Form(...), content: str = Form(...)):
    return_in_db = returns.read(tag=tag)
    if return_in_db:
        raise HTTPException(
            status_code=400, detail="Tag já existe, defina outra."
        )
    return returns.create(
        return_=schemas.Return(
            tag=tag,
            content=content,
        )
    )


@router.get("/{tag}", response_model=schemas.Return)
def read(tag: str):
    return_in_db = returns.read(tag=tag)
    if not return_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return return_in_db


@router.put("/{tag}", response_model=schemas.Return)
def update(tag: str, new_return: schemas.Return):
    return_in_db = returns.read(tag=tag)
    if not return_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return returns.update(tag=tag, new_return=new_return)


@router.delete("/{tag}")
def delete(tag: str):
    return_in_db = returns.read(tag=tag)
    if not return_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return returns.delete(tag=tag)


@router.get("/", response_model=List[schemas.Return])
def get(limit: int = 100):
    return returns.get(limit=limit)
