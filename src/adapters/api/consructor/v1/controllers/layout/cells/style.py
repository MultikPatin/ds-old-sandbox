from typing import Annotated

from common.core.enums import URLEnum
from common.core.exceptions import LockedOperationErrorContent
from common.core.protocols import SessionProtocol
from common.fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, status

from src.adapters.api.consructor.v1.schemas import (
    LayoutStyleCreateRequest,
    LayoutStyleResponse,
    LayoutStyleUpdateRequest,
)
from src.application.dtos.db import LayoutStyleCreateDTO, LayoutStyleUpdateDTO
from src.application.protocols import LayoutStyleServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.post(
    URLEnum.root,
    summary="Create a style layer item",
    response_model=LayoutStyleResponse,
)
async def add(
    body: Annotated[LayoutStyleCreateRequest, Body()],
    service: FromDishka[LayoutStyleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutStyleResponse:
    condition = LayoutStyleCreateDTO(**body.model_dump())
    obj = await service.add(condition, session=session)
    return LayoutStyleResponse(**obj.model_dump())


@router.get(
    URLEnum.id,
    summary="Return an existing style layer item",
    response_model=LayoutStyleResponse,
)
async def get(
    _id: Annotated[str, IDPath()],
    service: FromDishka[LayoutStyleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutStyleResponse:
    obj = await service.get(_id, session=session)
    return LayoutStyleResponse(**obj.model_dump())


@router.patch(
    URLEnum.id,
    summary="Update a style layer item",
    response_model=LayoutStyleResponse,
)
async def update(
    _id: Annotated[str, IDPath()],
    body: Annotated[LayoutStyleUpdateRequest, Body()],
    service: FromDishka[LayoutStyleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutStyleResponse:
    """
    When updating, the entity's ID may change.
    This is because entities are hashed, and if there is an existing record
    with the same hash, the entity will be replaced with the existing one.
    """
    condition = LayoutStyleUpdateDTO(**body.model_dump())
    obj = await service.update(_id, condition, session=session)
    return LayoutStyleResponse(**obj.model_dump())


@router.delete(
    URLEnum.id,
    summary="Delete an existing style layer item if no references to it",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_423_LOCKED: {"model": LockedOperationErrorContent},
    },
)
async def delete(
    _id: Annotated[str, IDPath()],
    service: FromDishka[LayoutStyleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> None:
    await service.delete(_id, session=session)
