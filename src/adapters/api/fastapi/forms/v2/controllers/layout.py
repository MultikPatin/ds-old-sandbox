from typing import Annotated

from common.core.enums import URLEnum
from common.fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.adapters.api.fastapi.forms.v2.schemas.layout import LayoutResponse
from src.application.protocols.services.layout import LayoutServiceProtocol

router = APIRouter(route_class=DishkaRoute)

# TODO Detail the documentation


@router.get(
    URLEnum.id,
    summary="Return an existing layout by id",
    response_model=LayoutResponse,
)
async def get(
    _id: Annotated[str, IDPath(description_prefix="Layout ID <br><br>")],
    service: FromDishka[LayoutServiceProtocol],
) -> LayoutResponse:
    layout = await service.get(_id)
    return LayoutResponse(**layout.model_dump())


@router.get(
    "/by-input" + URLEnum.id,
    summary="Return an existing layout by input_id",
    response_model=LayoutResponse,
)
async def get_by_input_id(
    _id: Annotated[str, IDPath(description_prefix="Input ID <br><br>")],
    service: FromDishka[LayoutServiceProtocol],
) -> LayoutResponse:
    layout = await service.get_by_input_id(_id)
    return LayoutResponse(**layout.model_dump())
