import json
from typing import List, Union
from loro.lib.utils import schemas
from loro.lib.utils.db.sql.models import Dialog
from pony.orm import db_session


def dialog_schema(dialog: Dialog) -> schemas.Dialog:
    return schemas.Dialog(
        tag=dialog.tag,
        header=dialog.header,
        choices=[
            schemas.Choice(**(json.loads(choice))) for choice in dialog.choices
        ],
        leads_to=dialog.leads_to,
    )


def dialog_dict(dialog: schemas.Dialog) -> dict:
    return dict(
        tag=dialog.tag,
        header=dialog.header,
        choices=[choice.json() for choice in dialog.choices],
        leads_to=dialog.leads_to,
    )


@db_session
def create_dialog(dialog: schemas.Dialog) -> schemas.Dialog:
    dialog_to_db = Dialog(**dialog_dict(dialog))
    return dialog_schema(dialog_to_db)


@db_session
def read_dialog(tag: str) -> Union[dict, schemas.Dialog]:
    try:
        return dialog_schema(Dialog.get(tag=tag))
    except:
        return dict()


@db_session
def update_dialog(tag: str, new_dialog: schemas.Dialog) -> schemas.Dialog:
    dialog_in_db = Dialog.get(tag=tag)
    dialog_in_db.update(**dialog_dict(new_dialog))

    return dialog_schema(dialog_in_db)


@db_session
def delete_dialog(tag: str) -> dict:
    dialog_in_db = Dialog.get(tag=tag)
    dialog_in_db.delete()
    return dict(delete="ok")


@db_session
def get_dialogs(limit: int) -> List[Union[dict, schemas.Dialog]]:
    try:
        dialogs = Dialog.select().order_by((Dialog.tag))[:limit]
        return [dialog_schema(dialog) for dialog in dialogs]
    except:
        return [dict()]
