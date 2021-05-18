# pylint:disable=missing-function-docstring
# pylint:disable=missing-module-docstring

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loro.core.config import settings

DOMAIN = settings.domain

app = FastAPI()
app.mount("/static", StaticFiles(directory="loro/web/static"), name="static")
templates = Jinja2Templates(directory="loro/web/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "domain": DOMAIN}
    )

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "domain": DOMAIN}
    )
