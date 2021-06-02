# pylint:disable=function-redefined

from loro.lib.utils import schemas
from loro.lib.utils.db.sql.crud import returns

from .router import (
    Form,
    HTMLResponse,
    RedirectResponse,
    Request,
    app,
    templates,
    status,
)


@app.get("/returns", response_class=HTMLResponse)
def get(request: Request, limit: int = 100):
    returns_ = returns.get(limit=limit)

    if returns_:
        return templates.TemplateResponse(
            "returns/returns.html",
            context={"request": request, "returns": returns_},
        )

    return templates.TemplateResponse(
        "returns/not_found.html", context={"request": request}
    )


@app.get("/returns/create", response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse(
        "returns/create_form.html",
        context={
            "request": request,
            "existent_tag": False,
            "tag": "",
            "formInputClass": "form-control",
            "content": "",
        },
    )


@app.post("/returns/create")
def create(request: Request, tag: str = Form(...), content: str = Form(...)):
    tag_already_exists = returns.read(tag=tag)
    if tag_already_exists:
        return templates.TemplateResponse(
            "returns/create_form.html",
            context={
                "request": request,
                "existent_tag": True,
                "tag": tag,
                "formInputClass": "form-control is-invalid",
                "content": content,
            },
        )

    return_ = schemas.Return(tag=tag, content=content)
    returns.create(return_)

    return RedirectResponse(
        url="/returns", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/returns/update/{tag}", response_class=HTMLResponse)
def update(request: Request, tag: str):
    current_return = returns.read(tag=tag)

    return templates.TemplateResponse(
        "returns/update_form.html",
        context={
            "request": request,
            "existent_tag": False,
            "tag": tag,
            "new_tag": "",
            "current_return": current_return,
            "new_return": current_return,
            "formInputClass": "form-control",
        },
    )


@app.post("/returns/update/{tag}")
def update(
    request: Request,
    tag: str,
    new_tag: str = Form(...),
    new_content: str = Form(...),
):
    new_return = schemas.Return(tag=new_tag, content=new_content)
    if new_tag != tag:
        tag_already_exists = returns.read(tag=new_tag)
        if tag_already_exists:
            current_return = returns.read(tag=tag)
            return templates.TemplateResponse(
                "returns/update_form.html",
                context={
                    "request": request,
                    "existent_tag": True,
                    "tag": tag,
                    "new_tag": new_tag,
                    "current_return": current_return,
                    "new_return": new_return,
                    "formInputClass": "form-control is-invalid",
                },
            )

    returns.update(tag=tag, new_return=new_return)

    return RedirectResponse(
        url="/returns", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/returns/delete", response_class=HTMLResponse)
def delete(tag: str):
    returns.delete(tag=tag)
    return RedirectResponse(url="/returns")
