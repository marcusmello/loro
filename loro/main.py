import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from loro.api.api_v1.api import api_router
from loro.core.config import settings

from loro.web.pages.routes import pages

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount('', pages)

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("loro.main:app", host="0.0.0.0", port=8000, reload=True)
