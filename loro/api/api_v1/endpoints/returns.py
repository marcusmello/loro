from typing import List

from fastapi import APIRouter, HTTPException
from loro.lib.utils import schemas
from loro.lib.utils.db.sql import crud

router = APIRouter()

@router.post("/", response_model=schemas.Return)
def create_return(return_: schemas.Return):
    return_in_db = crud.get_return_by_tag(tag=return_.tag)
    if return_in_db:
        raise HTTPException(status_code=400, detail="Tag já existe, defina outra.")
    return crud.create_return(return_=return_)

@router.get("/", response_model=List[schemas.Return])
def read_returns(limit: int = 100):
    returns = crud.get_returns(limit=limit)
    return returns

@router.get("/{tag}", response_model=schemas.Return)
def read_return_by_tag(tag: str):
    return_in_db = crud.get_return_by_tag(tag=tag)
    if not return_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return return_in_db
