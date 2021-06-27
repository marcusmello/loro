# pylint: skip-file

from __future__ import annotations

import json

from app.settings.general import settings
from app.lib.utils import schemas
from pony.orm import (
    Database,
    Json,
    LongStr,
    Optional,
    PrimaryKey,
    Required,
    Set,
    StrArray,
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


class Answer(db.Entity, AttributeUpdater):
    tag = Required(str, unique=True)
    header = Required(LongStr)
    choices = Optional(StrArray)


class Message(db.Entity):
    client = Optional(lambda: FinalClient)
    content = Required(LongStr)
    direction = Required(str)
    timestamp = Required(int)


class FinalClient(db.Entity):
    id = PrimaryKey(int)  # whatsapp number
    messages = Set(Message, cascade_delete=True)


db.generate_mapping(create_tables=True)
