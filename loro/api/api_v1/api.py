from fastapi import APIRouter
from loro.api.api_v1.endpoints import twilio_hook, answers

api_router = APIRouter()
api_router.include_router(twilio_hook.router, prefix="/twilio-hook")
api_router.include_router(answers.router, prefix="/answers")
