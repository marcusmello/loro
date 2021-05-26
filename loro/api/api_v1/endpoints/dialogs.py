from typing import List

from fastapi import APIRouter, HTTPException, Form
from loro.lib.utils import schemas
from loro.lib.utils.db.sql.crud import dialogs

router = APIRouter()


@router.post("/", response_model=schemas.Dialog)
def create_dialog(dialog: schemas.Dialog):
    dialog_in_db = dialogs.read_dialog(tag=dialog.tag)
    if dialog_in_db:
        raise HTTPException(
            status_code=400, detail="Tag já existe, defina outra."
        )

    return dialogs.create_dialog(dialog)


@router.get("/{tag}", response_model=schemas.Dialog)
def read_dialog(tag: str):
    dialog_in_db = dialogs.read_dialog(tag=tag)
    if not dialog_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return dialog_in_db


@router.put("/{tag}", response_model=schemas.Dialog)
def update_dialog(tag: str, new_dialog: schemas.Dialog):
    dialog_in_db = dialogs.read_dialog(tag=tag)
    if not dialog_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return dialogs.update_dialog(tag=tag, new_dialog=new_dialog)


@router.delete("/{tag}")
def delete(tag: str):
    dialog_in_db = dialogs.read_dialog(tag=tag)
    if not dialog_in_db:
        raise HTTPException(status_code=400, detail="Tag inexistente")
    return dialogs.delete_dialog(tag=tag)


@router.get("/", response_model=List[schemas.Dialog])
def get_dialogs(limit: int = 100):
    return dialogs.get_dialogs(limit=limit)
