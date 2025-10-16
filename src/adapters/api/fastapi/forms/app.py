from common.fastapi import App
from fastapi import FastAPI
from starlette.types import Lifespan

from .settings import Settings


class _App(App):
    def __init__(
        self,
        settings: Settings,
        lifespan: Lifespan[FastAPI] | None = None,
    ):
        super().__init__(settings, lifespan)
