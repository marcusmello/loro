from pony.orm import db_session

from typing import List

from fastapi import APIRouter, Request, HTTPException #, Response
from loro.lib.utils import schemas
from loro.lib.utils.db.sql import crud, models

router = APIRouter()

@router.post("/", response_model=schemas.Return)
@db_session
def create_return(return_: schemas.Return):
    #db_return = crud.get_return_by_tag(tag=return_.tag)
    #if db_return:
    #    raise HTTPException(status_code=400, detail="Tag já existe, defina outra.")
    return crud.create_return(return_=return_)

@router.get("/", response_model=List[schemas.Return])
def read_returns(limit: int = 100):
    returns = crud.get_returns(limit=limit)
    return returns
