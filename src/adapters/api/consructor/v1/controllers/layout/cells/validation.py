from typing import Annotated

from abgroup_core.enums import URLEnum
from abgroup_core.exceptions import LockedOperationErrorContent
from abgroup_core.protocols import SessionProtocol
from abgroup_fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, status

from src.adapters.api.consructor.v1.schemas import (
    LayoutValidationCreateRequest,
    LayoutValidationResponse,
    LayoutValidationUpdateRequest,
)
from src.application.dtos.db import (
    LayoutValidationCreateDTO,
    LayoutValidationUpdateDTO,
)
from src.application.protocols import LayoutValidationServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.post(
    URLEnum.root,
    summary="Create a validation layer item",
    response_model=LayoutValidationResponse,
)
async def add(
    body: Annotated[LayoutValidationCreateRequest, Body()],
    service: FromDishka[LayoutValidationServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutValidationResponse:
    condition = LayoutValidationCreateDTO(**body.model_dump())
    obj = await service.add(condition, session=session)
    return LayoutValidationResponse(**obj.model_dump())


@router.get(
    URLEnum.id,
    summary="Return an existing validation layer item",
    response_model=LayoutValidationResponse,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get(
    _id: Annotated[str, IDPath()],
    service: FromDishka[LayoutValidationServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutValidationResponse:
    layout = await service.get(_id, session=session)
    return LayoutValidationResponse(**layout.model_dump())


@router.patch(
    URLEnum.id,
    summary="Update a validation layer item",
    response_model=LayoutValidationResponse,
    deprecated=True,
)
async def update(
    _id: Annotated[str, IDPath()],
    body: Annotated[LayoutValidationUpdateRequest, Body()],
    service: FromDishka[LayoutValidationServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutValidationResponse:
    """
    When updating, the entity's ID may change.
    This is because entities are hashed, and if there is an existing record
    with the same hash, the entity will be replaced with the existing one.
    """
    condition = LayoutValidationUpdateDTO(**body.model_dump())
    obj = await service.update(_id, condition, session=session)
    return LayoutValidationResponse(**obj.model_dump())


@router.delete(
    URLEnum.id,
    summary="Delete an existing validation layer item if no references to it",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_423_LOCKED: {"model": LockedOperationErrorContent},
    },
    deprecated=True,
)
async def delete(
    _id: Annotated[str, IDPath()],
    service: FromDishka[LayoutValidationServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> None:
    await service.delete(_id, session=session)
