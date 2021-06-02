# pylint: skip-file
from typing import List
from loro.lib.utils import schemas
from loro.lib.utils.db.sql.models import Return
from pony.orm import db_session


@db_session
def create(return_: schemas.Return) -> dict:
    _return = Return(**return_.dict())
    return _return.to_dict()


@db_session
def read(tag: str) -> dict:
    try:
        return_in_db = Return.get(tag=tag)
        return return_in_db.to_dict()
    except:
        return dict()


@db_session
def update(tag: str, new_return: schemas.Return) -> dict:
    return_in_db = Return.get(tag=tag)
    return_in_db.update(**new_return.dict())
    return return_in_db.to_dict()


@db_session
def delete(tag: str) -> dict:
    return_in_db = Return.get(tag=tag)
    return_in_db.delete()
    return dict(delete="ok")


@db_session
def get(limit: int) -> List[dict]:
    try:
        returns = Return.select().order_by((Return.tag))[:limit]
        return [r.to_dict() for r in returns]
    except:
        return [dict()]
