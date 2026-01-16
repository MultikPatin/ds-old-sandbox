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
    LayoutMessageCursorFiltersRequest,
    LayoutMessageLimitOffsetFiltersRequest,
    LayoutMessagePagesFiltersRequest,
    LayoutMessageResponse,
)
from src.application.dtos.filters import (
    LayoutMessageCursorFilters,
    LayoutMessageLimitOffsetFilters,
    LayoutMessagePagesFilters,
)
from src.application.protocols import LayoutMessageServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.get(
    URLEnum.pagination_page,
    summary="Return existing unique massage blocks with pagination "
    "using the pages strategy",
    response_model=PagesPageResponse[LayoutMessageResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_pages(
    filters: Annotated[LayoutMessagePagesFiltersRequest, Query()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> PagesPageResponse[LayoutMessageResponse]:
    instance = await service.get_all_pages(
        filters=LayoutMessagePagesFilters(**filters.model_dump()),
        session=session,
    )
    return PagesPageResponse[LayoutMessageResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing unique massage blocks with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[LayoutMessageResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_limit_offset(
    filters: Annotated[LayoutMessageLimitOffsetFiltersRequest, Query()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LimitOffsetPageResponse[LayoutMessageResponse]:
    instance = await service.get_all_limit_offset(
        filters=LayoutMessageLimitOffsetFilters(**filters.model_dump()),
        session=session,
    )
    return LimitOffsetPageResponse[LayoutMessageResponse](
        **instance.model_dump()
    )


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing unique massage blocks with pagination "
    "using the cursor strategy",
    response_model=CursorPageResponse[LayoutMessageResponse],
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get_all_cursor(
    filters: Annotated[LayoutMessageCursorFiltersRequest, Query()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> CursorPageResponse[LayoutMessageResponse]:
    instance = await service.get_all_cursor(
        filters=LayoutMessageCursorFilters(**filters.model_dump()),
        session=session,
    )
    return CursorPageResponse[LayoutMessageResponse](**instance.model_dump())


@router.get(
    URLEnum.id,
    summary="Return an existing massage blocks",
    response_model=LayoutMessageResponse,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get(
    _id: Annotated[str, IDPath()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutMessageResponse:
    obj = await service.get(_id, session=session)
    return LayoutMessageResponse(**obj.model_dump())
