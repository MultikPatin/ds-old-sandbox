from http import HTTPStatus
from typing import Annotated

from common.core.enums import URLEnum
from common.core.protocols import SessionProtocol
from common.fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body

from src.adapters.api.fastapi.forms.v2.schemas.input import (
    InputSingleBulkResponse,
    InputSingleBulkUpdateSchema,
    InputSingleResponse,
)
from src.application.dtos.db.input import InputSingleUpdateDTO
from src.application.protocols.services.input import InputSingleServiceProtocol

router = APIRouter(route_class=DishkaRoute)

# TODO Детализировать документацию


@router.patch(
    URLEnum.root,
    summary="Update existing blocks",
    status_code=HTTPStatus.CREATED,
    response_model=InputSingleBulkResponse,
    # TODO Добавить ошибки валидации update параметров.
)
async def bulk_update(
    # TODO Вернуть при реализации валидации
    # TODO Определить необходимость передачи layout_id
    # filters: Annotated[schemas.InputUpdateFilter, Query()],
    body: Annotated[InputSingleBulkUpdateSchema, Body()],
    service: FromDishka[InputSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputSingleBulkResponse:
    # TODO Реализовать сервис валидации update параметров.
    instances = await service.bulk_update(
        [InputSingleUpdateDTO(**item.model_dump()) for item in body.items],
        session=session,
    )
    # TODO Реализовать transform у учётом аннотации протоколом
    # await transform(instance, filters.structure)
    return InputSingleBulkResponse(
        items=[
            InputSingleResponse(**instance.model_dump())
            for instance in instances
            if instance is not None
            # TODO После реализации исключений проверка на None будет не нужна
        ]
    )


@router.patch(
    URLEnum.id,
    summary="Update an existing block",
    status_code=HTTPStatus.CREATED,
    response_model=InputSingleResponse,
    # TODO Добавить ошибки валидации update параметров.
)
async def update(
    _id: Annotated[
        str, IDPath(description_prefix="Идентификатор блока <br><br>")
    ],
    # TODO Вернуть при реализации валидации
    # TODO Определить необходимость передачи layout_id
    # filters: Annotated[schemas.InputUpdateFilter, Query()]
    body: Annotated[InputSingleUpdateDTO, Body()],
    service: FromDishka[InputSingleServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputSingleResponse:
    # TODO Реализовать сервис валидации bulk_update параметров.
    condition = InputSingleUpdateDTO(**body.model_dump())
    instance = await service.update(_id, condition, session=session)
    # TODO Реализовать transform у учётом аннотации протоколом
    # await transform(instance, filters.structure)
    return InputSingleResponse(**instance.model_dump())
