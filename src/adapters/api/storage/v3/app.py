from common.fastapi import VApp
from fastapi import status

from .controllers import (
    input_cards_router,
    input_router,
    layout_cards_router,
    layout_router,
)
from .settings import Settings


class App(VApp):
    def __init__(self, is_dev_mode: bool, settings: Settings) -> None:
        super().__init__(is_dev_mode=is_dev_mode, settings=settings)

        layout_router.include_router(
            layout_cards_router,
            prefix="/cards",
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
        )
        self._api.include_router(
            router=layout_router,
            prefix="/layouts",
            tags=["Layout"],
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
        )
        input_router.include_router(
            input_cards_router,
            prefix="/cards",
            responses={
                status.HTTP_204_NO_CONTENT: {"model": None},
            },
        )
        self._api.include_router(
            router=input_router,
            prefix="/inputs",
            tags=["Input"],
        )
