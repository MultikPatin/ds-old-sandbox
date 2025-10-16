from typing import Annotated

from common.core.dtos.pagination import (
    CursorParamsDTO,
    LimitOffsetParamsDTO,
    PagesParamsDTO,
)
from common.core.enums import URLEnum
from common.fastapi.schemas.pagination import (
    CursorPageResponse,
    LimitOffsetPageResponse,
    PagesPageResponse,
)
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from src.adapters.api.fastapi.forms.v2.schemas.input import (
    InputCardCursorFilters,
    InputCardLimitOffsetFilters,
    InputCardPagesFilters,
    InputCardResponse,
)
from src.application.dtos.filters import InputCardFilters
from src.application.protocols.services.input import InputCardServiceProtocol

router = APIRouter(route_class=DishkaRoute)

# TODO Детализировать документацию
# TODO Добавить сортировку по месту


@router.get(
    URLEnum.pagination_page,
    summary="Return existing cards with pagination using the pages strategy",
    response_model=PagesPageResponse[InputCardResponse],
)
async def get_all_like_pages(
    filters: Annotated[InputCardPagesFilters, Query()],
    service: FromDishka[InputCardServiceProtocol],
) -> PagesPageResponse[InputCardResponse]:
    instance = await service.get_all_like_pages(
        params=PagesParamsDTO(number=filters.number, size=filters.size),
        filters=InputCardFilters(**filters.model_dump()),
    )
    return PagesPageResponse[InputCardResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing cards with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[InputCardResponse],
)
async def get_all_like_limit_offset(
    filters: Annotated[InputCardLimitOffsetFilters, Query()],
    service: FromDishka[InputCardServiceProtocol],
) -> LimitOffsetPageResponse[InputCardResponse]:
    instance = await service.get_all_like_limit_offset(
        params=LimitOffsetParamsDTO(limit=filters.limit, offset=filters.offset),
        filters=InputCardFilters(**filters.model_dump()),
    )
    return LimitOffsetPageResponse[InputCardResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing cards with pagination using the cursor strategy",
    response_model=CursorPageResponse[InputCardResponse],
)
async def get_all_like_cursor(
    filters: Annotated[InputCardCursorFilters, Query()],
    service: FromDishka[InputCardServiceProtocol],
) -> CursorPageResponse[InputCardResponse]:
    instance = await service.get_all_like_cursor(
        params=CursorParamsDTO(cursor=filters.cursor, size=filters.size),
        filters=InputCardFilters(**filters.model_dump()),
    )
    return CursorPageResponse[InputCardResponse](**instance.model_dump())
