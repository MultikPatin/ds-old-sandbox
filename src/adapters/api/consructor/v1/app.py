from abgroup_fastapi import VApp

from .controllers import (
    massage_router,
    schema_router,
    style_router,
    validation_router,
)
from .settings import Settings


class App(VApp):
    def __init__(self, is_dev_mode: bool, settings: Settings) -> None:
        super().__init__(is_dev_mode=is_dev_mode, settings=settings)

        # BLOCKS

        self._api.include_router(
            router=massage_router, prefix="/messages", tags=["Block message"]
        )

        # LAYERS

        self._api.include_router(
            router=schema_router, prefix="/schemas", tags=["Layer schema"]
        )
        self._api.include_router(
            router=validation_router,
            prefix="/validations",
            tags=["Layer validation"],
        )
        self._api.include_router(
            router=style_router, prefix="/styles", tags=["Layer style"]
        )
