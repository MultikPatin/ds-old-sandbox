from typing import Annotated

from common.core.enums import URLEnum
from common.core.protocols import SessionProtocol
from common.fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from src.adapters.api.storage.v3.schemas import (
    LayoutFiltersRequest,
    LayoutResponse,
)
from src.application.dtos.filters import (
    LayoutFilters,
)
from src.application.protocols import LayoutServiceProtocol

from .card import router as cards_router

router = APIRouter(route_class=DishkaRoute)
router.include_router(cards_router, prefix="/cards")


@router.get(
    URLEnum.id,
    summary="Return an existing layout",
    response_model=LayoutResponse,
)
async def get_with_layers(
    _id: Annotated[str, IDPath(description_prefix="Layout ID <br><br>")],
    filters: Annotated[LayoutFiltersRequest, Query()],
    service: FromDishka[LayoutServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutResponse:
    layout = await service.get_with_layers(
        _id=_id,
        filters=LayoutFilters(**filters.model_dump()),
        session=session,
    )
    return LayoutResponse(**layout.model_dump())


@router.get(
    "/by-input" + URLEnum.id,
    summary="Return an existing layout by input id",
    response_model=LayoutResponse,
)
async def get_by_input(
    _id: Annotated[str, IDPath(description_prefix="Input ID <br><br>")],
    filters: Annotated[LayoutFiltersRequest, Query()],
    service: FromDishka[LayoutServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutResponse:
    layout = await service.get_by_input(
        _id=_id,
        filters=LayoutFilters(**filters.model_dump()),
        session=session,
    )
    return LayoutResponse(**layout.model_dump())
