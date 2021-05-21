# pylint:disable=missing-function-docstring
# pylint:disable=missing-module-docstring
# pylint:disable=unused-import

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#from loro.core.config import settings
from loro.lib.utils.db.sql import crud

app = FastAPI()
app.mount("/static", StaticFiles(directory="loro/web/static"), name="static")
templates = Jinja2Templates(directory="loro/web/templates")
