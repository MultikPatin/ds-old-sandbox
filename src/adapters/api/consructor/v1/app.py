from common.fastapi import VApp
from fastapi import status

from .controllers import schema_router, style_router, validation_router
from .settings import Settings


class App(VApp):
    def __init__(self, is_dev_mode: bool, settings: Settings) -> None:
        super().__init__(is_dev_mode=is_dev_mode, settings=settings)

        self._api.include_router(
            router=schema_router,
            prefix="/schemas",
            tags=["Schema layer"],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
        )
        self._api.include_router(
            router=validation_router,
            prefix="/validations",
            tags=["Validation layer"],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
        )
        self._api.include_router(
            router=style_router,
            prefix="/styles",
            tags=["Style layer"],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
        )
