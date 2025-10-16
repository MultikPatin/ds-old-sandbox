from common.core.exceptions import NoContentError
from common.mongo import (
    Base,
    convert_to_dto,
    convert_to_dtos,
    convert_to_id,
)
from pymongo.asynchronous.client_session import AsyncClientSession

from src.application.dtos.db.key import KeyLinks


class KeyRepository(Base):
    async def get_by_model_id(
        self, model_id: str, *, session: AsyncClientSession | None = None
    ) -> list[KeyLinks]:
        documents = await self._collection.find_many(
            self._collection.model.id == convert_to_id(model_id),
            session=session,
        ).to_list()
        if documents is None:
            raise NoContentError
        return convert_to_dtos(documents, KeyLinks, replace_links=True)

    async def get_by_layout_id(
        self, layout_id: str, *, session: AsyncClientSession | None = None
    ) -> KeyLinks:
        document = await self._collection.find_one(
            self._collection.layout.id == convert_to_id(layout_id),
            session=session,
        )
        if document is None:
            raise NoContentError
        return convert_to_dto(document, KeyLinks, replace_links=True)
