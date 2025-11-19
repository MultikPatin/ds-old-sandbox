from typing import TYPE_CHECKING

from common.mongo.enums import KeysEnum
from common.mongo.utils import convert_to_dto

from .base import Base, BaseDTO
from .getters import _GetMixin

if TYPE_CHECKING:
    from beanie import Document
    from pydantic import BaseModel
    from pymongo.asynchronous.client_session import AsyncClientSession


class _UpdateMixin[UpdateSchema: BaseModel](_GetMixin, Base):
    async def _update(
        self,
        _id: str,
        condition: UpdateSchema,
        *,
        session: "AsyncClientSession",
    ) -> "Document":
        document = await self._get(_id, session=session)
        return await document.update(  # type: ignore
            {KeysEnum.set: condition.model_dump(exclude_unset=True)},
            session=session,
        )


class UpdateMixin[UpdateSchema: BaseModel, ReturnSchema: BaseModel](
    _UpdateMixin[UpdateSchema], BaseDTO[ReturnSchema]
):
    async def update(
        self,
        _id: str,
        condition: UpdateSchema,
        *,
        session: "AsyncClientSession",
    ) -> ReturnSchema:
        document = await self._update(_id, condition, session=session)
        return convert_to_dto(document, self._dto)


class UpdateWithReturnIdMixin[UpdateSchema: BaseModel](
    _UpdateMixin[UpdateSchema], Base
):
    async def update_with_return_id(
        self,
        _id: str,
        condition: UpdateSchema,
        *,
        session: "AsyncClientSession",
    ) -> str:
        document = await self._update(_id, condition, session=session)
        return str(document.id)
