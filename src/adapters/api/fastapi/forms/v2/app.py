from http import HTTPStatus

from common.fastapi import VersionedApp

from .controllers import (
    blocks_router,
    card_router,
    input_router,
    layout_router,
    model_router,
)
from .settings import Settings


class App(VersionedApp):
    def __init__(self, is_dev_mode: bool, settings: Settings) -> None:
        super().__init__(is_dev_mode=is_dev_mode, settings=settings)

        self._api.include_router(
            router=model_router,
            prefix="/models",
            tags=["Model"],
            responses={
                HTTPStatus.NO_CONTENT: {"model": None},
            },
        )
        self._api.include_router(
            router=layout_router,
            prefix="/layouts",
            tags=["Layout"],
            responses={
                HTTPStatus.NO_CONTENT: {"model": None},
            },
        )
        self._api.include_router(
            router=input_router,
            prefix="/inputs",
            tags=["Input"],
        )
        self._api.include_router(
            card_router,
            prefix="/cards",
            tags=["Input cards"],
            responses={
                HTTPStatus.NO_CONTENT: {"model": None},
            },
        )
        self._api.include_router(
            router=blocks_router,
            prefix="/blocks",
            tags=["Input blocks"],
        )
