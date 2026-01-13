from typing import TYPE_CHECKING

from abgroup_core.exceptions import NoContentError

from common.mongo.enums import KeysEnum
from common.mongo.utils import convert_to_id

from .base import Base

if TYPE_CHECKING:
    from pymongo.asynchronous.client_session import AsyncClientSession


class ExistsMixin(Base):
    async def exists(self, _id: str, *, session: "AsyncClientSession") -> bool:
        return await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
        ).exists()


class CountMixin(Base):
    async def count(self, *, session: "AsyncClientSession") -> int:
        return await self._collection.find_many(session=session).count()


class IncRefCountMixin(Base):
    async def inc_ref(self, _id: str, *, session: "AsyncClientSession") -> None:
        result = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)}, session=session
        ).update({KeysEnum.inc: {"ref_count": 1}}, session=session)

        if result.modified_count == 0:
            raise NoContentError


class DecRefCountMixin(Base):
    async def dec_ref(self, _id: str, *, session: "AsyncClientSession") -> None:
        result = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)}, session=session
        ).update({KeysEnum.inc: {"ref_count": -1}}, session=session)

        if result.modified_count == 0:
            raise NoContentError
