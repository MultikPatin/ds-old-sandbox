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
    LayoutTableCursorFiltersRequest,
    LayoutTableLimitOffsetFiltersRequest,
    LayoutTablePagesFiltersRequest,
    LayoutTableResponse,
    LayoutTableShortResponse,
)
from src.application.dtos.filters import (
    LayersFetcherFilters,
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
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_pages(
    query: Annotated[LayoutTablePagesFiltersRequest, Query()],
    service: FromDishka[LayoutTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> PagesPageResponse[LayoutTableShortResponse]:
    filters = LayoutTablePagesFilters(**query.model_dump())
    instance = await service.get_all_pages(filters, session=session)
    return PagesPageResponse[LayoutTableShortResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing unique table blocks with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[LayoutTableShortResponse],
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_limit_offset(
    query: Annotated[LayoutTableLimitOffsetFiltersRequest, Query()],
    service: FromDishka[LayoutTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LimitOffsetPageResponse[LayoutTableShortResponse]:
    filters = LayoutTableLimitOffsetFilters(**query.model_dump())
    instance = await service.get_all_limit_offset(filters, session=session)
    return LimitOffsetPageResponse[LayoutTableShortResponse](
        **instance.model_dump()
    )


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing unique table blocks with pagination "
    "using the cursor strategy",
    response_model=CursorPageResponse[LayoutTableShortResponse],
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_cursor(
    query: Annotated[LayoutTableCursorFiltersRequest, Query()],
    service: FromDishka[LayoutTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> CursorPageResponse[LayoutTableShortResponse]:
    filters = LayoutTableCursorFilters(**query.model_dump())
    instance = await service.get_all_cursor(filters, session=session)
    return CursorPageResponse[LayoutTableShortResponse](**instance.model_dump())


@router.get(
    URLEnum.id,
    summary="Return an existing table block",
    response_model=LayoutTableResponse,
)
async def get_with_layers(
    _id: Annotated[str, IDPath(description_prefix="Block identifier <br><br>")],
    query: Annotated[LayersFetcherFiltersRequest, Query()],
    service: FromDishka[LayoutTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutTableResponse:
    filters = LayersFetcherFilters(**query.model_dump())
    layout = await service.get_with_layers(_id, filters, session=session)
    return LayoutTableResponse(**layout.model_dump())
