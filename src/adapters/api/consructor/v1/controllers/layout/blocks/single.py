from typing import Annotated

from abgroup_core.enums import URLEnum
from abgroup_core.protocols import SessionProtocol
from abgroup_fastapi.annotations import IDPath
from abgroup_fastapi.schemas.pagination import (
    CursorPageResponse,
    LimitOffsetPageResponse,
    PagesPageResponse,
)
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from src.adapters.api.consructor.v1.schemas import (
    LayersFetcherFiltersRequest,
    LayoutSingleCursorFiltersRequest,
    LayoutSingleLimitOffsetFiltersRequest,
    LayoutSinglePagesFiltersRequest,
    LayoutSingleResponse,
    LayoutSingleShortResponse,
)
from src.application.dtos.filters import (
    LayersFetcherFilters,
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
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_pages(
    query: Annotated[LayoutSinglePagesFiltersRequest, Query()],
    service: FromDishka[LayoutSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> PagesPageResponse[LayoutSingleShortResponse]:
    filters = LayoutSinglePagesFilters(**query.model_dump())
    instance = await service.get_all_pages(filters, session=session)
    return PagesPageResponse[LayoutSingleShortResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing unique single blocks with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[LayoutSingleShortResponse],
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_limit_offset(
    query: Annotated[LayoutSingleLimitOffsetFiltersRequest, Query()],
    service: FromDishka[LayoutSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LimitOffsetPageResponse[LayoutSingleShortResponse]:
    filters = LayoutSingleLimitOffsetFilters(**query.model_dump())
    instance = await service.get_all_limit_offset(filters, session=session)
    return LimitOffsetPageResponse[LayoutSingleShortResponse](
        **instance.model_dump()
    )


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing unique single blocks with pagination "
    "using the cursor strategy",
    response_model=CursorPageResponse[LayoutSingleShortResponse],
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_cursor(
    query: Annotated[LayoutSingleCursorFiltersRequest, Query()],
    service: FromDishka[LayoutSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> CursorPageResponse[LayoutSingleShortResponse]:
    filters = LayoutSingleCursorFilters(**query.model_dump())
    instance = await service.get_all_cursor(filters, session=session)
    return CursorPageResponse[LayoutSingleShortResponse](
        **instance.model_dump()
    )


@router.get(
    URLEnum.id,
    summary="Return an existing single block",
    response_model=LayoutSingleResponse,
)
async def get_with_layers(
    _id: Annotated[str, IDPath(description_prefix="Block identifier <br><br>")],
    query: Annotated[LayersFetcherFiltersRequest, Query()],
    service: FromDishka[LayoutSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutSingleResponse:
    filters = LayersFetcherFilters(**query.model_dump())
    layout = await service.get_with_layers(_id, filters, session=session)
    return LayoutSingleResponse(**layout.model_dump())
