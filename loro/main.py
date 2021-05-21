import uvicorn
from fastapi import FastAPI

from loro.api.api_v1.api import api_router
from loro.core.config import settings
from loro.web.routes import router

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount('', router.app)


def start():
    """Launched with `poetry run loro` at root level"""
    uvicorn.run("loro.main:app", host="0.0.0.0", port=8000, reload=True)
