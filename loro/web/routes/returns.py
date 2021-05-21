from .router import app, templates, HTMLResponse, Request, crud

@app.get("/returns", response_class=HTMLResponse)
def read_returns(request: Request, limit: int = 100):
    returns = crud.get_returns(limit=limit)

    if returns:
        return templates.TemplateResponse(
        "returns/returns.html", {"request": request, "returns": returns}
        )

    return templates.TemplateResponse(
        "returns/not_found.html", {"request": request}
        )
