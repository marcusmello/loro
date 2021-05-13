from fastapi import FastAPI

from loro.api.api_v1.api import api_router
from loro.core.config import settings

#from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)
