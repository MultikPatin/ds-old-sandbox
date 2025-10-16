from common.core.exceptions import NoContentError
from common.mongo import (
    Base,
    KeysEnum,
    convert_to_dto,
    convert_to_id,
)
from pymongo.asynchronous.client_session import AsyncClientSession

from src.application.dtos.db.layout import LayoutFullLinks


class LayoutRepository(Base):
    async def get(
        self, _id: str, *, session: AsyncClientSession | None = None
    ) -> LayoutFullLinks:
        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
            fetch_links=True,
            nesting_depths_per_field={
                "inputs": 0,
                "keys": 0,
                "card": 1,
                "singles": 3,
                "tables": 4,
            },
        )
        if document is None:
            raise NoContentError
        return convert_to_dto(document, LayoutFullLinks)
