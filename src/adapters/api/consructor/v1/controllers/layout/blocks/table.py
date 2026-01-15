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
from fastapi import APIRouter, Query, status

from src.adapters.api.consructor.v1.schemas import (
    LayoutTableCursorFiltersRequest,
    LayoutTableLimitOffsetFiltersRequest,
    LayoutTablePagesFiltersRequest,
    LayoutTableShortResponse,
)
from src.application.dtos.filters import (
    LayoutTableCursorFilters,
    LayoutTableLimitOffsetFilters,
    LayoutTablePagesFilters,
)
from src.application.protocols import LayoutTableServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.get(
    URLEnum.pagination_page,
    summary="Return existing unique table blocks with pagination "
    "using the pages strategy",
    response_model=PagesPageResponse[LayoutTableShortResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_pages(
    filters: Annotated[LayoutTablePagesFiltersRequest, Query()],
    service: FromDishka[LayoutTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> PagesPageResponse[LayoutTableShortResponse]:
    instance = await service.get_all_pages(
        filters=LayoutTablePagesFilters(**filters.model_dump()),
        session=session,
    )
    return PagesPageResponse[LayoutTableShortResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing unique table blocks with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[LayoutTableShortResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_limit_offset(
    filters: Annotated[LayoutTableLimitOffsetFiltersRequest, Query()],
    service: FromDishka[LayoutTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LimitOffsetPageResponse[LayoutTableShortResponse]:
    instance = await service.get_all_limit_offset(
        filters=LayoutTableLimitOffsetFilters(**filters.model_dump()),
        session=session,
    )
    return LimitOffsetPageResponse[LayoutTableShortResponse](
        **instance.model_dump()
    )


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing unique table blocks with pagination "
    "using the cursor strategy",
    response_model=CursorPageResponse[LayoutTableShortResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_cursor(
    filters: Annotated[LayoutTableCursorFiltersRequest, Query()],
    service: FromDishka[LayoutTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> CursorPageResponse[LayoutTableShortResponse]:
    instance = await service.get_all_cursor(
        filters=LayoutTableCursorFilters(**filters.model_dump()),
        session=session,
    )
    return CursorPageResponse[LayoutTableShortResponse](**instance.model_dump())
