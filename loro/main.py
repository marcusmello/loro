import uvicorn
from fastapi import FastAPI

from loro.api.api_v1.api import api_router
from loro.core.config import settings
from loro.web.routes import router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000/returns",
    "http://localhost:8000/returns/create",
    "http://localhost:8000",
    "http://0.0.0.0:8000",
    "http://127.0.0.1:8000",
]

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount('', router.app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def start():
    """Launched with `poetry run loro` at root level"""
    uvicorn.run("loro.main:app", host="0.0.0.0", port=8000, reload=True)
