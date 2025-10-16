from typing import Annotated

from common.core.dtos.pagination import (
    CursorParamsDTO,
    LimitOffsetParamsDTO,
    PagesParamsDTO,
)
from common.core.enums import URLEnum
from common.fastapi.annotations import IDPath
from common.fastapi.schemas.pagination import (
    CursorPageResponse,
    LimitOffsetPageResponse,
    PagesPageResponse,
)
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from src.adapters.api.fastapi.forms.v2.schemas.model import (
    ModelCursorFilters,
    ModelLimitOffsetFilters,
    ModelPagesFilters,
    ModelResponse,
)
from src.application.dtos.filters import ModelFilters
from src.application.protocols.services.model import ModelServiceProtocol

router = APIRouter(route_class=DishkaRoute)

# TODO Добавить сортировку по месту
SORT_STUB = "title"


@router.get(
    "/by-layout" + URLEnum.id,
    summary="Return the existing model by layout_id",
    response_model=ModelResponse,
)
async def get_by_layout_id(
    _id: Annotated[str, IDPath(description_prefix="Layout ID <br><br>")],
    service: FromDishka[ModelServiceProtocol],
) -> ModelResponse:
    model = await service.get_by_layout_id(_id)
    return ModelResponse(**model.model_dump())


@router.get(
    URLEnum.pagination_page,
    summary="Return existing models with pagination using the pages strategy",
    response_model=PagesPageResponse[ModelResponse],
)
async def get_all_like_pages(
    filters: Annotated[ModelPagesFilters, Query()],
    service: FromDishka[ModelServiceProtocol],
) -> PagesPageResponse[ModelResponse]:
    instance = await service.get_all_like_pages(
        params=PagesParamsDTO(number=filters.number, size=filters.size),
        filters=ModelFilters(**filters.model_dump(), sort=SORT_STUB),
    )
    return PagesPageResponse[ModelResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing models with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[ModelResponse],
)
async def get_all_like_limit_offset(
    filters: Annotated[ModelLimitOffsetFilters, Query()],
    service: FromDishka[ModelServiceProtocol],
) -> LimitOffsetPageResponse[ModelResponse]:
    instance = await service.get_all_like_limit_offset(
        params=LimitOffsetParamsDTO(limit=filters.limit, offset=filters.offset),
        filters=ModelFilters(**filters.model_dump(), sort=SORT_STUB),
    )
    return LimitOffsetPageResponse[ModelResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing models with pagination using the cursor strategy",
    response_model=CursorPageResponse[ModelResponse],
)
async def get_all_like_cursor(
    filters: Annotated[ModelCursorFilters, Query()],
    service: FromDishka[ModelServiceProtocol],
) -> CursorPageResponse[ModelResponse]:
    instance = await service.get_all_like_cursor(
        params=CursorParamsDTO(cursor=filters.cursor, size=filters.size),
        filters=ModelFilters(**filters.model_dump(), sort=SORT_STUB),
    )
    return CursorPageResponse[ModelResponse](**instance.model_dump())
