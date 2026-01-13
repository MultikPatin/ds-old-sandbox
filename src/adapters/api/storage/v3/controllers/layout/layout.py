from typing import Annotated

from abgroup_core.enums import URLEnum
from abgroup_core.protocols import SessionProtocol
from abgroup_fastapi.annotations import IDPath
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

router = APIRouter(route_class=DishkaRoute)


@router.get(
    URLEnum.id,
    summary="Return an existing layout",
    response_model=LayoutResponse,
)
async def get_with_layers(
    _id: Annotated[
        str, IDPath(description_prefix="Layout identifier <br><br>")
    ],
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
    _id: Annotated[str, IDPath(description_prefix="Input identifier <br><br>")],
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
