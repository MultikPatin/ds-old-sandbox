from common.fastapi import VApp
from fastapi import status

from .controllers import input_router, layout_router
from .settings import Settings


class App(VApp):
    def __init__(self, is_dev_mode: bool, settings: Settings) -> None:
        super().__init__(is_dev_mode=is_dev_mode, settings=settings)

        self._api.include_router(
            router=layout_router,
            prefix="/layouts",
            tags=["Layout"],
            responses={
                status.HTTP_202_ACCEPTED: {"model": None},
            },
        )
        self._api.include_router(
            router=input_router,
            prefix="/inputs",
            tags=["Input"],
        )
