from app.core.config import settings

# from app.lib.utils import schemas
from app.lib.utils.db.sql.crud import answers

from .answers_dynamic_form import (
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

paths = settings.url_paths.answers

DYNAMIC_FORM = "answers/dynamic_form.html"
dynamic_context = DynamicContext()
parse_form = ParseForm()


@app.get(paths.root, response_class=HTMLResponse)
def get(request: Request, limit: int = 100):
    answers_in_db = answers.get_collection(limit=limit)

    if answers_in_db:
        return templates.TemplateResponse(
            "answers/answers.html",
            context={"request": request, "answers": answers_in_db},
        )

    return templates.TemplateResponse(
        "answers/not_found.html", context={"request": request}
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
    answer = parse_form.from_raw_form(answer_form=form.multi_items())

    if not (answer.tag and answer.header):
        raise HTTPException(status_code=502)

    tag_already_exists = answers.read(tag=answer.tag)
    if tag_already_exists:
        raise HTTPException(status_code=403)

    answers.create(answer)


@app.get(path=paths.create_error + "/{data}")
def invalid_create(request: Request, data: str):
    answers = parse_form.from_raw_invalid_input(data=data)

    return templates.TemplateResponse(
        DYNAMIC_FORM,
        context=dynamic_context.invalid_create(request, answers),
    )

@app.get(path=paths.update + "/{tag}", response_class=HTMLResponse)
def update(request: Request, tag:str):
    answer_to_update = answers.read(tag=tag)

    return templates.TemplateResponse(
        DYNAMIC_FORM,
        context=dynamic_context.default_update(request, tag, answer_to_update),
    )

@app.post(path=paths.update + "/{tag}")
async def update(request: Request, tag:str):
    form = await request.form()
    new_answers = parse_form.from_raw_form(answer_form=form.multi_items())

    if not (new_answers.tag and new_answers.header):
        raise HTTPException(status_code=502)

    if new_answers.tag != tag:
        tag_already_exists = answers.read(tag=new_answers.tag)
        if tag_already_exists:
            raise HTTPException(status_code=403)

    answers.update(tag=tag, new_answer=new_answers)


@app.get(path=paths.update_error + "/{tag}/{data}")
def invalid_update(request: Request, tag: str, data: str):
    answer_to_update = parse_form.from_raw_invalid_input(data=data)

    return templates.TemplateResponse(
        DYNAMIC_FORM,
        context=dynamic_context.invalid_update(request, tag, answer_to_update),
    )

@app.get(path=paths.delete + "/{tag}", response_class=HTMLResponse)
def delete(tag: str):
    answers.delete(tag=tag)
    return RedirectResponse(url=paths.root, status_code=status.HTTP_303_SEE_OTHER)
