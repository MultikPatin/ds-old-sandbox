from typing import Annotated

from abgroup_core.enums import URLEnum
from abgroup_core.protocols import SessionProtocol
from abgroup_fastapi.schemas.pagination import (
    CursorPageResponse,
    LimitOffsetPageResponse,
    PagesPageResponse,
)
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query

from src.adapters.api.storage.v3.schemas import (
    InputCardCursorFiltersRequest,
    InputCardLimitOffsetFiltersRequest,
    InputCardPagesFiltersRequest,
    InputCardResponse,
)
from src.application.dtos.filters import (
    InputCardCursorFilters,
    InputCardLimitOffsetFilters,
    InputCardPagesFilters,
)
from src.application.protocols import InputCardServiceProtocol

router = APIRouter(route_class=DishkaRoute)

# TODO Детализировать документацию
# TODO Добавить сортировку по месту


@router.get(
    URLEnum.pagination_page,
    summary="Return existing cards with pagination using the pages strategy",
    response_model=PagesPageResponse[InputCardResponse],
)
async def get_all_pages(
    filters: Annotated[InputCardPagesFiltersRequest, Query()],
    service: FromDishka[InputCardServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> PagesPageResponse[InputCardResponse]:
    instance = await service.get_all_pages(
        filters=InputCardPagesFilters(**filters.model_dump()),
        session=session,
    )
    return PagesPageResponse[InputCardResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing cards with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[InputCardResponse],
)
async def get_all_limit_offset(
    filters: Annotated[InputCardLimitOffsetFiltersRequest, Query()],
    service: FromDishka[InputCardServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LimitOffsetPageResponse[InputCardResponse]:
    instance = await service.get_all_limit_offset(
        filters=InputCardLimitOffsetFilters(**filters.model_dump()),
        session=session,
    )
    return LimitOffsetPageResponse[InputCardResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing cards with pagination using the cursor strategy",
    response_model=CursorPageResponse[InputCardResponse],
)
async def get_all_cursor(
    filters: Annotated[InputCardCursorFiltersRequest, Query()],
    service: FromDishka[InputCardServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> CursorPageResponse[InputCardResponse]:
    instance = await service.get_all_cursor(
        filters=InputCardCursorFilters(**filters.model_dump()),
        session=session,
    )
    return CursorPageResponse[InputCardResponse](**instance.model_dump())
