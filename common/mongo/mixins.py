import asyncio
from collections.abc import Sequence, Set
from typing import TYPE_CHECKING

from beanie.operators import In

from common.core.enums import LifeStatusEnum
from common.core.exceptions import NoContentError
from common.core.utils import time_now

from .enums import KeysEnum
from .utils import convert_to_dto, convert_to_dtos, convert_to_id, set_batches

if TYPE_CHECKING:
    from beanie import Document
    from pydantic import BaseModel
    from pymongo.asynchronous.client_session import AsyncClientSession


class Base:
    def __init__[DocType: Document](self, collection: type[DocType]):
        self._collection = collection


class BaseDTO[ReturnSchema: BaseModel](Base):
    def __init__[DocType: Document](
        self, collection: type[DocType], dto: type[ReturnSchema]
    ):
        super().__init__(collection)
        self._dto = dto


class _GetMixin(Base):
    async def _get(
        self, _id: str, *, session: "AsyncClientSession"
    ) -> "Document":
        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
        )
        if not document:
            raise NoContentError
        return document


class GetMixin[ReturnSchema: BaseModel](_GetMixin, BaseDTO[ReturnSchema]):
    async def get(
        self, _id: str, *, session: "AsyncClientSession"
    ) -> ReturnSchema:
        document = await self._get(_id, session=session)
        return convert_to_dto(document, self._dto, is_replace_links=True)


class GetByIDsMixin[ReturnSchema: BaseModel](BaseDTO[ReturnSchema]):
    async def get_by_ids(
        self,
        ids: Sequence[str] | Set[str],
        *,
        session: "AsyncClientSession",
        batch_size: int | None = None,
        max_concurrent: int = 25,
    ) -> list[ReturnSchema]:
        if isinstance(ids, Set):
            ids = list(ids)

        batches = set_batches(ids, batch_size)

        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_batch(batch_ids: Sequence[str]) -> list[ReturnSchema]:
            async with semaphore:
                docs = await self._collection.find_many(
                    In(KeysEnum.id, [convert_to_id(_id) for _id in batch_ids]),
                    session=session,
                ).to_list()
                return convert_to_dtos(docs, self._dto, is_replace_links=True)

        tasks = [process_batch(batch) for batch in batches]

        documents = []
        for coro in asyncio.as_completed(tasks):
            documents.extend(await coro)

        return documents


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


class DeleteMixin(_GetMixin):
    async def delete(self, _id: str, *, session: "AsyncClientSession") -> str:
        document = await self._get(_id, session=session)
        await document.delete(session=session)
        return _id


class DeleteSoftMixin(_GetMixin):
    async def delete_soft(
        self, _id: str, *, session: "AsyncClientSession"
    ) -> str:
        document = await self._get(_id, session=session)

        if not hasattr(document, "status"):
            msg = "Document has no status attribute"
            raise AssertionError(msg)
        if not isinstance(document.status, LifeStatusEnum):
            msg = "Status attribute is not an instance of LifeStatusEnum"
            raise TypeError(msg)

        document.status = LifeStatusEnum.deleted

        # TODO: конкретизировать назначение и тип полей
        if hasattr(document, "deleted_at"):
            document.deleted_at = time_now()
        if hasattr(document, "deleted"):
            if isinstance(document.deleted, bool):
                document.deleted = True
            else:
                document.deleted = time_now()
        if hasattr(document, "updated_at"):
            document.updated_at = time_now()
        if hasattr(document, "updated"):
            if isinstance(document.updated, bool):
                document.updated = True
            else:
                document.updated = time_now()
        await document.save_changes(session=session)
        return _id


class ExistsMixin(Base):
    async def exists(self, _id: str, *, session: "AsyncClientSession") -> bool:
        return await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
        ).exists()


class CountMixin(Base):
    async def count(self, *, session: "AsyncClientSession") -> int:
        return await self._collection.find_many(session=session).count()
