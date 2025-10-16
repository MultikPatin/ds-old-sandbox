from http import HTTPStatus
from typing import Annotated

from common.core.enums import URLEnum
from common.core.protocols import SessionProtocol
from common.fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body

from src.adapters.api.fastapi.forms.v2.schemas.input import (
    InputTableBulkResponse,
    InputTableBulkUpdate,
    InputTableResponse,
)
from src.application.dtos.db.input import InputTableUpdateDTO
from src.application.protocols.services.input import InputTableServiceProtocol

router = APIRouter(route_class=DishkaRoute)

# TODO Детализировать документацию


@router.patch(
    URLEnum.root,
    summary="Update existing blocks",
    status_code=HTTPStatus.CREATED,
    response_model=InputTableBulkResponse,
    # TODO Добавить ошибки валидации update параметров.
)
async def bulk_update(
    # TODO Вернуть при реализации валидации
    # TODO Определить необходимость передачи layout_id
    # filters: Annotated[schemas.InputUpdateFilter, Query()],
    body: Annotated[InputTableBulkUpdate, Body()],
    service: FromDishka[InputTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputTableBulkResponse:
    # TODO Реализовать сервис валидации bulk_update параметров.
    # TODO Реализовать сервис валидации update параметров.
    instances = await service.bulk_update(
        [InputTableUpdateDTO(**item.model_dump()) for item in body.items],
        session=session,
    )
    # TODO Реализовать transform у учётом аннотации протоколом
    # await transform(instance, filters.structure)
    return InputTableBulkResponse(
        items=[
            InputTableResponse(**instance.model_dump())
            for instance in instances
            if instance is not None
            # TODO После реализации исключений проверка на None будет не нужна
        ]
    )


@router.patch(
    URLEnum.id,
    summary="Update an existing block",
    status_code=HTTPStatus.CREATED,
    response_model=InputTableResponse,
    # TODO Добавить ошибки валидации update параметров.
)
async def update(
    _id: Annotated[
        str, IDPath(description_prefix="Идентификатор блока <br><br>")
    ],
    # TODO Вернуть при реализации валидации
    # TODO Определить необходимость передачи layout_id
    # filters: Annotated[schemas.InputUpdateFilter, Query()]
    body: Annotated[InputTableUpdateDTO, Body()],
    service: FromDishka[InputTableServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputTableResponse:
    # TODO Реализовать сервис валидации bulk_update параметров.
    condition = InputTableUpdateDTO(**body.model_dump())
    instance = await service.update(_id, condition, session=session)
    # TODO Реализовать transform у учётом аннотации протоколом
    # await transform(instance, filters.structure)
    return InputTableResponse(**instance.model_dump())
