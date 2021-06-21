import uvicorn
from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.web.pages import router
from fastapi.middleware.cors import CORSMiddleware
from app.lib.chatbot import create_default_answers_if_they_do_not_exist


app = FastAPI()
app.include_router(api_router, prefix=settings.API_prefix_version)
app.mount("", router.app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.generate(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    create_default_answers_if_they_do_not_exist()
    # settings startup


def start():
    """Launched with `poetry run loro` at root level"""
    uvicorn.run(
        "loro.main:app",
        host=settings.cors_origins.main_domain,
        port=settings.cors_origins.main_port,
        reload=True,
    )
