#pylint:disable=missing-module-docstring

from fastapi import FastAPI
from loro.web.pages import items, home

pages = FastAPI()
pages.mount("/items", items.app)
pages.mount("", home.app)
