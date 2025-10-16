from common.fastapi import VersionedApp

from .controllers import hello_router
from .settings import Settings


class App(VersionedApp):
    def __init__(self, is_dev_mode: bool, settings: Settings) -> None:
        super().__init__(is_dev_mode=is_dev_mode, settings=settings)

        self._api.include_router(
            router=hello_router,
            prefix="/hello",
            tags=["Hello"],
        )
