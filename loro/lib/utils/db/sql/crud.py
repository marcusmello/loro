# pylint: skip-file
from loro.lib.utils import schemas
from loro.lib.utils.db.sql import models
from pony.orm import db_session


@db_session
def create_return(return_: schemas.Return):
    _return = models.Return(tag=return_.tag, content=return_.content)
    return _return.to_dict()

@db_session
def get_return_by_tag(tag: str):
    try:
        return_in_db = models.Return.get(tag=tag)
        return return_in_db.to_dict()
    except:
        return dict()

@db_session
def get_returns(limit:int):
    try:
        return [r.to_dict() for r in models.Return.select()[:limit]]
    except:
        return dict()
