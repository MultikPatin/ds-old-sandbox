from beanie import Document
from pydantic import BaseModel
from pymongo.asynchronous.client_session import AsyncClientSession

from common.core.exceptions import NoContentError

from .documents import DocType
from .enums import KeysEnum
from .utils import convert_to_dto, convert_to_id


class Base:
    def __init__(self, collection: type[DocType]):
        self._collection = collection


class BaseDTO[ReturnSchema: BaseModel](Base):
    def __init__(self, collection: type[DocType], dto: type[ReturnSchema]):
        super().__init__(collection)
        self._dto = dto


class _GetMixin(Base):
    async def _get(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> Document:
        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
        )
        if document is None:
            raise NoContentError
        return document


class GetMixin[ReturnSchema: BaseModel](_GetMixin, BaseDTO[ReturnSchema]):
    async def get(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> ReturnSchema:
        document = await self._get(_id, session=session)
        return convert_to_dto(document, self._dto)


class AddMixin[CreateSchema: BaseModel, ReturnSchema: BaseModel](
    BaseDTO[ReturnSchema]
):
    async def add(
        self,
        condition: CreateSchema,
        *,
        session: AsyncClientSession | None = None,
    ) -> ReturnSchema:
        document = self._collection(**condition.model_dump(exclude_unset=True))
        document = await document.create(session=session)
        return convert_to_dto(document, self._dto)


class UpdateMixin[UpdateSchema: BaseModel, ReturnSchema: BaseModel](
    _GetMixin, BaseDTO[ReturnSchema]
):
    async def update(
        self,
        _id: str,
        condition: UpdateSchema,
        *,
        session: AsyncClientSession | None = None,
    ) -> ReturnSchema:
        document = await self._get(_id, session=session)
        document = await document.update(
            {KeysEnum.set: condition.model_dump(exclude_unset=True)},
            session=session,
        )
        return convert_to_dto(document, self._dto)


class DeleteMixin(_GetMixin):
    async def delete(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> str:
        document = await self._get(_id, session=session)
        await document.delete(session=session)
        return _id


class ExistsMixin(Base):
    async def exists(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> bool:
        return await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
        ).exists()


class CountMixin(Base):
    async def count(self, *, session: AsyncClientSession | None = None) -> int:
        return await self._collection.find_many(session=session).count()
