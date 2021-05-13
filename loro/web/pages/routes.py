from fastapi import FastAPI
from loro.web.pages import items

pages = FastAPI()
pages.mount("/items", items.app)
