from typing import Annotated

from abgroup_core.enums import LifeStatusEnum, URLEnum
from abgroup_core.exceptions import BusinessLogicErrorContent
from abgroup_core.protocols import SessionProtocol
from abgroup_fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from src.adapters.api.storage.v3.schemas import (
    InputResponse,
    InputStatusResponse,
)
from src.application.protocols import InputServiceProtocol

router = APIRouter(route_class=DishkaRoute)


@router.patch(
    URLEnum.id + URLEnum.status,
    summary="Update the status of an existing input",
    status_code=status.HTTP_201_CREATED,
    response_model=InputStatusResponse,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": BusinessLogicErrorContent},
    },
)
async def update_status(
    _id: Annotated[str, IDPath(description_prefix="Input identifier <br><br>")],
    service: FromDishka[InputServiceProtocol],
    session: FromDishka[SessionProtocol],
    value: Annotated[
        LifeStatusEnum,
        Query(
            alias="status",
            title="Status",
            description="Status value to set in the input <br><br>",
        ),
    ] = LifeStatusEnum.archived,
) -> InputStatusResponse:
    return InputStatusResponse(
        id=_id,
        status=await service.update_status(
            _id=_id, status=value, session=session
        ),
    )


@router.post(
    URLEnum.root,
    summary="Create an input as template",
    response_model=InputResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        # TODO Ошибка не корректного ключа макета
        # status.HTTP_400_BAD_REQUEST: {"model": BusinessLogicErrorContent},
    },
)
async def add_as_template(
    layout_key: Annotated[
        str,
        Query(
            alias="layout_key",
            title="Layout key",
            description="Key to find published layout <br><br>",
            min_length=1,
            max_length=32,
        ),
    ],
    service: FromDishka[InputServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputResponse:
    instance = await service.add_as_template(layout_key, session=session)
    return InputResponse(**instance.model_dump())


@router.get(
    URLEnum.id,
    summary="Return an existing input",
    response_model=InputResponse,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def get(
    _id: Annotated[str, IDPath(description_prefix="Input identifier <br><br>")],
    service: FromDishka[InputServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputResponse:
    instance = await service.get_with_values(_id, session=session)
    return InputResponse(**instance.model_dump())


@router.delete(
    URLEnum.id,
    summary="Soft delete an existing input",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def delete_soft(
    _id: Annotated[str, IDPath(description_prefix="Input identifier <br><br>")],
    service: FromDishka[InputServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> None:
    await service.delete_soft(_id, session=session)
