from loro.core.config import settings

# from loro.lib.utils import schemas
from loro.lib.utils.db.sql.crud import dialogs

from .dialogs_dynamic_form import (
    DynamicContext,
    ParseForm,
)
from .router import (
    HTMLResponse,
    RedirectResponse,
    Request,
    app,
    status,
    templates,
    HTTPException,
)

paths = settings.url_paths.dialogs

DYNAMIC_FORM = "dialogs/dynamic_form.html"
dynamic_context = DynamicContext()
parse_form = ParseForm()


@app.get(paths.root, response_class=HTMLResponse)
def get(request: Request, limit: int = 100):
    dialogs_in_db = dialogs.get_dialogs(limit=limit)

    if dialogs_in_db:
        return templates.TemplateResponse(
            "dialogs/dialogs.html",
            context={"request": request, "dialogs": dialogs_in_db},
        )

    return templates.TemplateResponse(
        "dialogs/not_found.html", context={"request": request}
    )


@app.get(paths.create, response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse(
        DYNAMIC_FORM,
        context=dynamic_context.default_create(request),
    )


@app.post(paths.create)
async def create(request: Request):
    form = await request.form()
    dialog = parse_form.from_raw_form(dialog_form=form.multi_items())

    if not (dialog.tag and dialog.header):
        raise HTTPException(status_code=502)

    tag_already_exists = dialogs.read_dialog(tag=dialog.tag)
    if tag_already_exists:
        raise HTTPException(status_code=403)

    dialogs.create_dialog(dialog)


@app.get(path=paths.create_error + "/{data}")
def invalid_create(request: Request, data: str):
    dialog = parse_form.from_raw_invalid_input(data=data)

    return templates.TemplateResponse(
        DYNAMIC_FORM,
        context=dynamic_context.invalid_create(request, dialog),
    )

@app.get(path=paths.update + "/{tag}", response_class=HTMLResponse)
def update(request: Request, tag:str):
    dialog_to_update = dialogs.read_dialog(tag=tag)

    return templates.TemplateResponse(
        DYNAMIC_FORM,
        context=dynamic_context.default_update(request, tag, dialog_to_update),
    )

@app.post(path=paths.update + "/{tag}")
async def update(request: Request, tag:str):
    form = await request.form()
    new_dialog = parse_form.from_raw_form(dialog_form=form.multi_items())

    if not (new_dialog.tag and new_dialog.header):
        raise HTTPException(status_code=502)

    if new_dialog.tag != tag:
        tag_already_exists = dialogs.read_dialog(tag=new_dialog.tag)
        if tag_already_exists:
            raise HTTPException(status_code=403)

    dialogs.update_dialog(tag=tag, new_dialog=new_dialog)


@app.get(path=paths.update_error + "/{tag}/{data}")
def invalid_update(request: Request, tag: str, data: str):
    dialog_to_update = parse_form.from_raw_invalid_input(data=data)

    return templates.TemplateResponse(
        DYNAMIC_FORM,
        context=dynamic_context.invalid_update(request, tag, dialog_to_update),
    )

@app.get(path=paths.delete + "/{tag}", response_class=HTMLResponse)
def delete(tag: str):
    dialogs.delete_dialog(tag=tag)
    return RedirectResponse(url=paths.root, status_code=status.HTTP_303_SEE_OTHER)
