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
    LayoutShortCursorFiltersRequest,
    LayoutShortLimitOffsetFiltersRequest,
    LayoutShortPagesFiltersRequest,
    LayoutShortResponse,
)
from src.application.dtos.filters import (
    LayoutShortCursorFilters,
    LayoutShortLimitOffsetFilters,
    LayoutShortPagesFilters,
)
from src.application.protocols import LayoutServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.get(
    URLEnum.pagination_page,
    summary="Return existing unique layouts with pagination "
    "using the pages strategy",
    response_model=PagesPageResponse[LayoutShortResponse],
)
async def get_all_pages(
    filters: Annotated[LayoutShortPagesFiltersRequest, Query()],
    service: FromDishka[LayoutServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> PagesPageResponse[LayoutShortResponse]:
    instance = await service.get_all_pages(
        filters=LayoutShortPagesFilters(**filters.model_dump()),
        session=session,
    )
    return PagesPageResponse[LayoutShortResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing unique layouts with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[LayoutShortResponse],
)
async def get_all_limit_offset(
    filters: Annotated[LayoutShortLimitOffsetFiltersRequest, Query()],
    service: FromDishka[LayoutServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LimitOffsetPageResponse[LayoutShortResponse]:
    instance = await service.get_all_limit_offset(
        filters=LayoutShortLimitOffsetFilters(**filters.model_dump()),
        session=session,
    )
    return LimitOffsetPageResponse[LayoutShortResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing unique layouts with pagination "
    "using the cursor strategy",
    response_model=CursorPageResponse[LayoutShortResponse],
)
async def get_all_cursor(
    filters: Annotated[LayoutShortCursorFiltersRequest, Query()],
    service: FromDishka[LayoutServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> CursorPageResponse[LayoutShortResponse]:
    instance = await service.get_all_cursor(
        filters=LayoutShortCursorFilters(**filters.model_dump()),
        session=session,
    )
    return CursorPageResponse[LayoutShortResponse](**instance.model_dump())
