from typing import Annotated

from common.core.enums import URLEnum
from common.core.protocols import SessionProtocol
from common.fastapi.annotations import IDPath
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from src.adapters.api.storage.v3.schemas import InputResponse
from src.application.protocols import InputServiceProtocol

from .card import router as cards_router

router = APIRouter(route_class=DishkaRoute)
router.include_router(cards_router, prefix="/cards")


@router.post(
    URLEnum.root,
    summary="Create an input as template",
    response_model=InputResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={},
    deprecated=True,
)
async def add_as_template(
    layout_key: Annotated[
        str, Query(description_prefix="Идентификатор макета <br><br>")
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
    _id: Annotated[
        str, IDPath(description_prefix="Идентификатор отчёта <br><br>")
    ],
    service: FromDishka[InputServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> InputResponse:
    instance = await service.get_with_values(_id, session=session)
    return InputResponse(**instance.model_dump())


@router.delete(
    URLEnum.id,
    summary="Sort delete an existing input",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def delete_soft(
    _id: Annotated[
        str, IDPath(description_prefix="Идентификатор отчёта <br><br>")
    ],
    service: FromDishka[InputServiceProtocol],
    session: FromDishka[SessionProtocol],
) -> None:
    await service.delete_soft(_id, session=session)
