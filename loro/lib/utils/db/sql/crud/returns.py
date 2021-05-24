# pylint: skip-file
from loro.lib.utils import schemas
from loro.lib.utils.db.sql import models
from pony.orm import db_session


@db_session
def create(return_: schemas.Return):
    _return = models.Return(tag=return_.tag, content=return_.content)
    return _return.to_dict()

@db_session
def read(tag: str):
    try:
        return_in_db = models.Return.get(tag=tag)
        return return_in_db.to_dict()
    except:
        return dict()

@db_session
def update(tag: str, new_return: schemas.Return):
    return_in_db = models.Return.get(tag=tag)
    return_in_db.update(**new_return.dict())
    return return_in_db.to_dict()

@db_session
def delete(tag: str):
    return_in_db = models.Return.get(tag=tag)
    return_in_db.delete()
    return dict(tag="", content= "")

@db_session
def get(limit: int):
    try:
        return [r.to_dict() for r in models.Return.select()[:limit]]
    except:
        return dict()
