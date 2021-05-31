from loro.core.config import settings

# from loro.lib.utils import schemas
from loro.lib.utils.db.sql.crud import dialogs

from .dialogs_dynamic_form import (
    DynamicForm,
    ParseForm,
)
from .router import (
    HTMLResponse,
    # RedirectResponse,
    Request,
    app,
    # status,
    templates,
    HTTPException,
)

paths = settings.url_paths.dialogs
dynamic_form = DynamicForm()
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
        "dialogs/dynamic_form.html",
        context=dynamic_form.empty_create(request),
    )


@app.post(paths.create)
async def create(request: Request):
    form = await request.form()
    dialog = parse_form.from_raw_form(dialog_form=form.multi_items())

    tag_already_exists = dialogs.read_dialog(tag=dialog.tag)
    if tag_already_exists:
        raise HTTPException(status_code=400)

    dialogs.create_dialog(dialog)


@app.get(path=paths.create_error + "/{data}")
def invalid_create(request: Request, data: str):
    dialog = parse_form.from_raw_invalid_input(data=data)

    return templates.TemplateResponse(
        "dialogs/dynamic_form.html",
        context=dynamic_form.invalid_create(request, dialog),
    )
