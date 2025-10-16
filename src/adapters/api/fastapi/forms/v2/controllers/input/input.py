from http import HTTPStatus
from typing import Annotated

from common.core.enums import URLEnum
from common.core.protocols import SessionProtocol
from common.fastapi.annotations import IDPath, IDQuery
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body

from src.adapters.api.fastapi.forms.v2.schemas.input import (
    InputSingleResponse,
    InputStatusResponse,
    InputStatusUpdateSchema,
    InputTableInMatrixResponse,
    InputUpdateSchema,
    InputWithTableInMatrixResponse,
)
from src.application.dtos.db.input import InputUpdateDTO, InputWithTableInMatrix
from src.application.protocols.services.input import (
    InputServiceProtocol,
    InputTemplateServiceProtocol,
)

router = APIRouter(route_class=DishkaRoute)

# TODO Детализировать документацию


@router.post(
    URLEnum.template,
    summary="Create an input template",
    response_model=InputWithTableInMatrixResponse,
    status_code=HTTPStatus.CREATED,
    responses={},
)
async def add_template(
    _id: Annotated[
        str, IDQuery(description_prefix="Идентификатор макета <br><br>")
    ],
    service: FromDishka[InputTemplateServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputWithTableInMatrixResponse:
    instance = await service.generate(layout_id=_id, session=session)
    # TODO Реализовать BackgroundTask на обновление счётчика ссылок в layout
    return await generate_response(instance)


@router.patch(
    URLEnum.id,
    summary="Update an existing input",
    status_code=HTTPStatus.CREATED,
    response_model=InputWithTableInMatrixResponse,
    responses={
        HTTPStatus.NO_CONTENT: {"model": None},
        # TODO Добавить ошибки валидации update параметров.
    },
)
async def update(
    _id: Annotated[
        str, IDPath(description_prefix="Идентификатор отчёта <br><br>")
    ],
    body: Annotated[InputUpdateSchema, Body()],
    service: FromDishka[InputServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputWithTableInMatrixResponse:
    # TODO Реализовать сервис валидации update параметров.
    condition = InputUpdateDTO(**body.model_dump())
    instance = await service.update(_id, condition, session=session)
    return await generate_response(instance)


@router.get(
    URLEnum.id,
    summary="Return an existing input by id",
    response_model=InputWithTableInMatrixResponse,
    responses={
        HTTPStatus.NO_CONTENT: {"model": None},
    },
)
async def get(
    _id: Annotated[
        str, IDPath(description_prefix="Идентификатор отчёта <br><br>")
    ],
    service: FromDishka[InputServiceProtocol],
) -> InputWithTableInMatrixResponse:
    instance = await service.get(_id)
    return await generate_response(instance)


@router.patch(
    URLEnum.id + URLEnum.status,
    summary="Update the status of an existing input",
    status_code=HTTPStatus.CREATED,
    response_model=InputStatusResponse,
    responses={
        HTTPStatus.NO_CONTENT: {"model": None},
    },
)
async def update_status(
    _id: Annotated[
        str, IDPath(description_prefix="Идентификатор отчёта <br><br>")
    ],
    body: Annotated[InputStatusUpdateSchema, Body()],
    service: FromDishka[InputServiceProtocol],
) -> InputStatusResponse:
    status = await service.update_status(_id=_id, status=body.status)
    return InputStatusResponse(id=_id, status=status)


@router.delete(
    URLEnum.id,
    summary="Delete an existing input",
    status_code=HTTPStatus.ACCEPTED,
    responses={
        HTTPStatus.NO_CONTENT: {"model": None},
    },
)
async def delete(
    _id: Annotated[
        str, IDPath(description_prefix="Идентификатор отчёта <br><br>")
    ],
    service: FromDishka[InputServiceProtocol],
) -> None:
    await service.delete(_id)


async def generate_response(
    instance: InputWithTableInMatrix,
) -> InputWithTableInMatrixResponse:
    return InputWithTableInMatrixResponse(
        **instance.model_dump(exclude={"singles", "tables"}),
        singles=[
            InputSingleResponse(**item.model_dump())
            for item in instance.singles
        ]
        if instance.singles
        else None,
        tables=[
            InputTableInMatrixResponse(**item.model_dump())
            for item in instance.tables
        ]
        if instance.tables
        else None,
    )
