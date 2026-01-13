import asyncio
from collections.abc import Sequence, Set
from typing import TYPE_CHECKING

from abgroup_core.exceptions import NoContentError
from beanie.operators import In

from common.mongo.enums import KeysEnum
from common.mongo.utils import (
    convert_to_dto,
    convert_to_dtos,
    convert_to_id,
    generate_batches,
)

from .base import Base, BaseDTO
from .projections import ProjectionID

if TYPE_CHECKING:
    from beanie import Document, PydanticObjectId
    from pydantic import BaseModel
    from pymongo.asynchronous.client_session import AsyncClientSession


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


class _GetByHasMixin(Base):
    def _get_by_hash(self, _hash: str) -> None:
        if not hasattr(self._collection, "hash"):
            msg = "Collection has no hash field"
            raise AttributeError(msg)


class GetByHashMixin[ReturnSchema: BaseModel](
    _GetByHasMixin, BaseDTO[ReturnSchema]
):
    async def get_by_hash(
        self, _hash: str, *, session: "AsyncClientSession"
    ) -> ReturnSchema:
        self._get_by_hash(_hash)
        document = await self._collection.find_one(
            {"hash": _hash},
            session=session,
        )
        if document is None:
            raise NoContentError
        return convert_to_dto(document, self._dto, is_replace_links=True)


class GetByHashWithReturnIdMixin(_GetByHasMixin):
    async def get_by_hash_with_return_id(
        self, _hash: str, *, session: "AsyncClientSession"
    ) -> str:
        self._get_by_hash(_hash)
        document = await self._collection.find_one(
            {"hash": _hash},
            session=session,
            projection_model=ProjectionID,
        )
        if document is None:
            raise NoContentError
        return document.id


class GetByIDsMixin[ReturnSchema: BaseModel](BaseDTO[ReturnSchema]):
    async def get_by_ids(
        self,
        ids: Sequence[str] | Set[str],
        *,
        session: "AsyncClientSession",
        batch_size: int | None = None,
        max_concurrent: int = 25,
    ) -> list[ReturnSchema]:
        if not ids:
            msg = "Must provide at least one id"
            # TODO: Реализовать специфическую ошибку
            raise ValueError(msg)

        converted_ids = [convert_to_id(_id) for _id in ids]
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process(
            _ids: Sequence["PydanticObjectId"],
        ) -> list[ReturnSchema]:
            async with semaphore:
                docs = await self._collection.find_many(
                    In(KeysEnum.id, _ids), session=session
                ).to_list()
                return convert_to_dtos(docs, self._dto, is_replace_links=True)

        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(process(b))
                for b in generate_batches(converted_ids, batch_size)
            ]

        documents = []
        for t in tasks:
            documents.extend(t.result())

        return documents
