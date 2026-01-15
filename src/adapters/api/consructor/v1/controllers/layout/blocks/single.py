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
    LayoutSingleCursorFiltersRequest,
    LayoutSingleLimitOffsetFiltersRequest,
    LayoutSinglePagesFiltersRequest,
    LayoutSingleShortResponse,
)
from src.application.dtos.filters import (
    LayoutSingleCursorFilters,
    LayoutSingleLimitOffsetFilters,
    LayoutSinglePagesFilters,
)
from src.application.protocols import LayoutSingleServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.get(
    URLEnum.pagination_page,
    summary="Return existing unique single blocks with pagination "
    "using the pages strategy",
    response_model=PagesPageResponse[LayoutSingleShortResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_pages(
    filters: Annotated[LayoutSinglePagesFiltersRequest, Query()],
    service: FromDishka[LayoutSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> PagesPageResponse[LayoutSingleShortResponse]:
    instance = await service.get_all_pages(
        filters=LayoutSinglePagesFilters(**filters.model_dump()),
        session=session,
    )
    return PagesPageResponse[LayoutSingleShortResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing unique single blocks with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[LayoutSingleShortResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_limit_offset(
    filters: Annotated[LayoutSingleLimitOffsetFiltersRequest, Query()],
    service: FromDishka[LayoutSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LimitOffsetPageResponse[LayoutSingleShortResponse]:
    instance = await service.get_all_limit_offset(
        filters=LayoutSingleLimitOffsetFilters(**filters.model_dump()),
        session=session,
    )
    return LimitOffsetPageResponse[LayoutSingleShortResponse](
        **instance.model_dump()
    )


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing unique single blocks with pagination "
    "using the cursor strategy",
    response_model=CursorPageResponse[LayoutSingleShortResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_cursor(
    filters: Annotated[LayoutSingleCursorFiltersRequest, Query()],
    service: FromDishka[LayoutSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> CursorPageResponse[LayoutSingleShortResponse]:
    instance = await service.get_all_cursor(
        filters=LayoutSingleCursorFilters(**filters.model_dump()),
        session=session,
    )
    return CursorPageResponse[LayoutSingleShortResponse](
        **instance.model_dump()
    )
