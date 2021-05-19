#pylint:disable=missing-module-docstring

from fastapi import FastAPI
from loro.web.pages import home

pages = FastAPI()
pages.mount("", home.app)
