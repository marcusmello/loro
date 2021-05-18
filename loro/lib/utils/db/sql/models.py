# pylint: skip-file

import json

from loro.core.config import settings
from pony.orm import (
    Database,
    Json,
    LongStr,
    Optional,
    Required,
    Set,
    commit,
    sql_debug,
    PrimaryKey,
)

db = Database()
db.bind(**settings.relational_database.dict())
sql_debug(settings.relational_database.sql_debug)


class AttributeUpdater(object):
    def update(self, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)
            commit()


class Interaction(db.Entity, AttributeUpdater):
    type_ = Required(str)
    tag = Required(str)


class Choice(db.Entity, AttributeUpdater):
    interaction = Optional(Interaction)
    text = Required(LongStr)
    leads_to = Optional(str)  # Interaction tags


class Dialog(Interaction):
    type_ = "d"
    text = Required(LongStr)
    choices: Set(Choice, cascade_delete=True)
    leads_to = Optional(str)  # Interaction tags


class Return(Interaction):
    type_ = "r"
    content = Required(str)


class Message(db.Entity):
    client = Optional(lambda: FinalClient)
    content = Required(LongStr)
    direction = Required(str)
    timestamp = Required(int)


class FinalClient(db.Entity):
    id = PrimaryKey(int)  # whatsapp number
    messages = Set(Message, cascade_delete=True)


db.generate_mapping(create_tables=True)
