from common.core.exceptions import NoContentError
from common.mongo import (
    AddMixin,
    GetMixin,
    convert_to_dto,
    convert_to_id,
)
from pymongo.asynchronous.client_session import AsyncClientSession

from src.application.dtos.db.layout import LayoutCardCreate, LayoutCardDB


class LayoutCardRepository(
    GetMixin[LayoutCardDB],
    AddMixin[LayoutCardCreate, LayoutCardDB],
):
    async def get_by_layout_id(
        self, layout_id: str, *, session: AsyncClientSession | None = None
    ) -> LayoutCardDB:
        document = await self._collection.find_one(
            self._collection.layout.id == convert_to_id(layout_id),
            session=session,
            fetch_links=True,
            nesting_depths_per_field={"layout": 1},
        )
        if document is None:
            raise NoContentError
        return convert_to_dto(document, LayoutCardDB)
