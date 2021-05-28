from loro.lib.utils import schemas
from loro.lib.utils.db.sql.crud import dialogs

from .dialogs_dynamic_fields_form import CHOICE_INPUT
from .router import (
    Form,
    HTMLResponse,
    RedirectResponse,
    Request,
    app,
    status,
    templates,
)


@app.get("/dialogs", response_class=HTMLResponse)
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


@app.get("/dialogs/create", response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse(
        "dialogs/create_form.html",
        context={
            "request": request,
            "existent_tag": False,
            "tag": "",
            "formInputClass": "form-control",
            "content": "",
            "choiceInput": CHOICE_INPUT,
        },
    )


@app.post("/dialogs/create")
async def create(request: Request):
    # tag_already_exists = returns.read(tag=tag)
    # if tag_already_exists:
    #    return templates.TemplateResponse(
    #        "returns/create_form.html",
    #        context={"request": request, "existent_tag": True, "tag": tag},
    #    )

    # return_ = schemas.Return(tag=tag, content=content)
    # returns.create(return_)

    # return RedirectResponse(
    #    url="/returns", status_code=status.HTTP_303_SEE_OTHER
    # )
    form = await request.form()

    for item in form.multi_items():
        print(item[1])

    # return RedirectResponse(
    #    url="/dialogs", status_code=status.HTTP_303_SEE_OTHER
    # )
