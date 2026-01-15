from abgroup_fastapi import VApp
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from .controllers import (
    # card_router,
    massage_router,
    schema_router,
    single_router,
    style_router,
    # table_router,
    validation_router,
)
from .settings import Settings

# BLOCKS

blocks_router = APIRouter(route_class=DishkaRoute)

# blocks_router.include_router(router=card_router, prefix="/cards")
blocks_router.include_router(router=massage_router, prefix="/messages")
blocks_router.include_router(router=single_router, prefix="/singles")
# blocks_router.include_router(router=table_router, prefix="/tables")

# LAYERS

layers_router = APIRouter(route_class=DishkaRoute)

layers_router.include_router(router=schema_router, prefix="/schemas")
layers_router.include_router(router=validation_router, prefix="/validations")
layers_router.include_router(router=style_router, prefix="/styles")


class App(VApp):
    def __init__(self, is_dev_mode: bool, settings: Settings) -> None:
        super().__init__(is_dev_mode=is_dev_mode, settings=settings)

        self._api.include_router(
            router=blocks_router, prefix="/blocks", tags=["Blocks of layout"]
        )

        self._api.include_router(
            router=layers_router, prefix="/layers", tags=["Layers of blocks"]
        )
