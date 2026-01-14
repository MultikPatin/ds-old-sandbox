from typing import Annotated

from abgroup_core.enums import URLEnum
from abgroup_core.exceptions import LockedOperationErrorContent
from abgroup_core.protocols import SessionProtocol
from abgroup_fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, status

from src.adapters.api.consructor.v1.schemas import (
    LayoutSchemaCreateRequest,
    LayoutSchemaResponse,
    LayoutSchemaUpdateRequest,
)
from src.application.dtos.db import LayoutSchemaCreateDTO, LayoutSchemaUpdateDTO
from src.application.protocols import LayoutSchemaServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.post(
    URLEnum.root,
    summary="Create a schema layer item",
    response_model=LayoutSchemaResponse,
)
async def add(
    body: Annotated[LayoutSchemaCreateRequest, Body()],
    service: FromDishka[LayoutSchemaServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutSchemaResponse:
    condition = LayoutSchemaCreateDTO(**body.model_dump())
    obj = await service.add(condition, session=session)
    return LayoutSchemaResponse(**obj.model_dump())


@router.get(
    URLEnum.id,
    summary="Return an existing schema layer item",
    response_model=LayoutSchemaResponse,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get(
    _id: Annotated[str, IDPath()],
    service: FromDishka[LayoutSchemaServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutSchemaResponse:
    obj = await service.get(_id, session=session)
    return LayoutSchemaResponse(**obj.model_dump())


@router.patch(
    URLEnum.id,
    summary="Update a schema layer item",
    response_model=LayoutSchemaResponse,
    deprecated=True,
)
async def update(
    _id: Annotated[str, IDPath()],
    body: Annotated[LayoutSchemaUpdateRequest, Body()],
    service: FromDishka[LayoutSchemaServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> LayoutSchemaResponse:
    """
    When updating, the entity's ID may change.
    This is because entities are hashed, and if there is an existing record
    with the same hash, the entity will be replaced with the existing one.
    """
    condition = LayoutSchemaUpdateDTO(**body.model_dump())
    obj = await service.update(_id, condition, session=session)
    return LayoutSchemaResponse(**obj.model_dump())


@router.delete(
    URLEnum.id,
    summary="Delete an existing schema layer item if no references to it",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_423_LOCKED: {"model": LockedOperationErrorContent},
    },
    deprecated=True,
)
async def delete(
    _id: Annotated[str, IDPath()],
    service: FromDishka[LayoutSchemaServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> None:
    await service.delete(_id, session=session)
