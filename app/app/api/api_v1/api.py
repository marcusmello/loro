from fastapi import APIRouter
from app.api.api_v1.endpoints import twilio_hook, answers
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(
    twilio_hook.router, prefix=settings.twilio.callback_hook_path
)
api_router.include_router(
    answers.router, prefix=settings.url_paths.answers.root
)
