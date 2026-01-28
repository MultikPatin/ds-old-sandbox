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
from fastapi import APIRouter, Body, Query, status

from src.adapters.api.consructor.v1.schemas import (
    LayoutMessageCreateRequest,
    LayoutMessageCursorFiltersRequest,
    LayoutMessageLimitOffsetFiltersRequest,
    LayoutMessagePagesFiltersRequest,
    LayoutMessageResponse,
    LayoutMessageUpdateRequest,
)
from src.application.dtos import LayoutMessageCreate
from src.application.dtos.db import LayoutMessageUpdateDTO
from src.application.dtos.filters import (
    LayoutMessageCursorFilters,
    LayoutMessageLimitOffsetFilters,
    LayoutMessagePagesFilters,
)
from src.application.protocols import LayoutMessageServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.get(
    URLEnum.pagination_page,
    summary="Return existing unique message blocks with pagination "
    "using the pages strategy",
    response_model=PagesPageResponse[LayoutMessageResponse],
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_pages(
    query: Annotated[LayoutMessagePagesFiltersRequest, Query()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> PagesPageResponse[LayoutMessageResponse]:
    filters = LayoutMessagePagesFilters(**query.model_dump())
    instance = await service.get_all_pages(filters, session=session)
    return PagesPageResponse[LayoutMessageResponse](**instance.model_dump())


@router.get(
    URLEnum.pagination_limit_offset,
    summary="Return existing unique message blocks with pagination "
    "using the limit offset strategy",
    response_model=LimitOffsetPageResponse[LayoutMessageResponse],
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_limit_offset(
    query: Annotated[LayoutMessageLimitOffsetFiltersRequest, Query()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LimitOffsetPageResponse[LayoutMessageResponse]:
    filters = LayoutMessageLimitOffsetFilters(**query.model_dump())
    instance = await service.get_all_limit_offset(filters, session=session)
    return LimitOffsetPageResponse[LayoutMessageResponse](
        **instance.model_dump()
    )


@router.get(
    URLEnum.pagination_cursor,
    summary="Return existing unique message blocks with pagination "
    "using the cursor strategy",
    response_model=CursorPageResponse[LayoutMessageResponse],
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get_all_cursor(
    query: Annotated[LayoutMessageCursorFiltersRequest, Query()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> CursorPageResponse[LayoutMessageResponse]:
    filters = LayoutMessageCursorFilters(**query.model_dump())
    instance = await service.get_all_cursor(filters, session=session)
    return CursorPageResponse[LayoutMessageResponse](**instance.model_dump())


@router.post(
    URLEnum.root,
    summary="Create a message blocks",
    response_model=LayoutMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add(
    body: Annotated[LayoutMessageCreateRequest, Body()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutMessageResponse:
    condition = LayoutMessageCreate(**body.model_dump())
    instance = await service.add(condition, session=session)
    return LayoutMessageResponse(**instance.model_dump())


@router.patch(
    URLEnum.id,
    summary="Update a message blocks",
    response_model=LayoutMessageResponse,
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
    status_code=status.HTTP_201_CREATED,
)
async def update(
    _id: Annotated[str, IDPath()],
    body: Annotated[LayoutMessageUpdateRequest, Body()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutMessageResponse:
    condition = LayoutMessageUpdateDTO(**body.model_dump(exclude_unset=True))
    instance = await service.update(_id, condition, session=session)
    return LayoutMessageResponse(**instance.model_dump())


@router.get(
    URLEnum.id,
    summary="Return an existing message blocks",
    response_model=LayoutMessageResponse,
    responses={status.HTTP_204_NO_CONTENT: {"model": None}},
)
async def get(
    _id: Annotated[str, IDPath()],
    service: FromDishka[LayoutMessageServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutMessageResponse:
    instance = await service.get(_id, session=session)
    return LayoutMessageResponse(**instance.model_dump())
