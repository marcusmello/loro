# pylint: skip-file

from __future__ import annotations

import json

from loro.core.config import settings
from loro.lib.utils import schemas
from pony.orm import (
    Database,
    Json,
    LongStr,
    Optional,
    PrimaryKey,
    Required,
    Set,
    commit,
    sql_debug,
)

db = Database()
db.bind(**settings.relational_database.dict())
sql_debug(settings.sql_debug)


class AttributeUpdater(object):
    def update(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)
            commit()


class Choice(db.Entity, AttributeUpdater):
    dialog = Optional(lambda: Dialog)
    text = Required(LongStr)
    leads_to = Optional(str)  # Interaction (Dialog or Return) tag


class Dialog(db.Entity, AttributeUpdater):
    tag = Required(str, unique=True)
    header = Required(LongStr)
    choices = Set(Choice, cascade_delete=True)
    leads_to = Optional(str)  # Interaction (Dialog or Return) tag


class Return(db.Entity, AttributeUpdater):
    tag = Required(str, unique=True)
    content = Required(str)

    @staticmethod
    def create(return_: schemas.Return) -> Return:

        _return = Return(tag=return_.tag, content=return_.content)
        commit()

        return Return[_return.id]


class Message(db.Entity):
    client = Optional(lambda: FinalClient)
    content = Required(LongStr)
    direction = Required(str)
    timestamp = Required(int)


class FinalClient(db.Entity):
    id = PrimaryKey(int)  # whatsapp number
    messages = Set(Message, cascade_delete=True)


db.generate_mapping(create_tables=True)
