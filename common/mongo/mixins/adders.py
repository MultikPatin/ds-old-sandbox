from typing import TYPE_CHECKING

from common.mongo.utils import convert_to_dto

from .base import Base, BaseDTO

if TYPE_CHECKING:
    from beanie import Document
    from pydantic import BaseModel
    from pymongo.asynchronous.client_session import AsyncClientSession


class _AddMixin[CreateSchema: BaseModel](Base):
    async def _add(
        self, condition: CreateSchema, *, session: "AsyncClientSession"
    ) -> "Document":
        document = self._collection(**condition.model_dump(exclude_none=True))
        return await document.create(session=session)


class AddMixin[CreateSchema: BaseModel, ReturnSchema: BaseModel](
    _AddMixin[CreateSchema], BaseDTO[ReturnSchema]
):
    async def add(
        self, condition: CreateSchema, *, session: "AsyncClientSession"
    ) -> ReturnSchema:
        document = await self._add(condition, session=session)
        return convert_to_dto(document, self._dto)


class AddWithReturnIdMixin[CreateSchema: BaseModel](
    _AddMixin[CreateSchema], Base
):
    async def add_with_return_id(
        self, condition: CreateSchema, *, session: "AsyncClientSession"
    ) -> str:
        document = await self._add(condition, session=session)
        return str(document.id)
