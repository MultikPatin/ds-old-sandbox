import asyncio
from collections.abc import Iterable
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
        return convert_to_dto(document, self._dto, is_replace_links=True)


class AddWithReturnIdMixin[CreateSchema: BaseModel](
    _AddMixin[CreateSchema], Base
):
    async def add_with_return_id(
        self, condition: CreateSchema, *, session: "AsyncClientSession"
    ) -> str:
        document = await self._add(condition, session=session)
        return str(document.id)


class BulkAddWithReturnIdMixin[CreateSchema: BaseModel](Base):
    async def bulk_add_with_return_id(
        self,
        conditions: Iterable[CreateSchema],
        *,
        session: "AsyncClientSession",
    ) -> list[str]:
        documents = (
            self._collection(**c.model_dump(exclude_none=True))
            for c in conditions
        )
        result = await self._collection.insert_many(documents, session=session)
        return [str(_id) for _id in result.inserted_ids if _id is not None]


class BulkAddMixin[CreateSchema: BaseModel, ReturnSchema: BaseModel](
    BaseDTO[ReturnSchema]
):
    async def bulk_add(
        self,
        conditions: Iterable[CreateSchema],
        *,
        session: "AsyncClientSession",
        max_concurrent: int = 25,
    ) -> list[ReturnSchema]:
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process(
            condition: CreateSchema, dto_class: type[ReturnSchema]
        ) -> ReturnSchema:
            async with semaphore:
                document = self._collection(
                    **condition.model_dump(exclude_none=True)
                )
                await document.create(session=session)
                return convert_to_dto(
                    document, dto_class, is_replace_links=True
                )

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(process(b, self._dto)) for b in conditions]
            if not tasks:
                msg = (
                    "Must provide at least one condition to process in bulk_add"
                )
                # TODO: Реализовать специфическую ошибку
                raise ValueError(msg)

        return [t.result() for t in tasks]
