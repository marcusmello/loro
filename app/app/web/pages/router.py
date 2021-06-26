# pylint:disable=missing-function-docstring
# pylint:disable=missing-module-docstring
# pylint:disable=unused-import

from fastapi import FastAPI, Form, Request, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#from app.settings.general import settings

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")
templates = Jinja2Templates(directory="app/web/templates")
