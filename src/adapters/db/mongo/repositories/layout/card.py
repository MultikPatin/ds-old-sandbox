from typing import TYPE_CHECKING

from common.core.exceptions import NoContentError
from common.mongo import (
    AddMixin,
    GetMixin,
    convert_to_dto,
    convert_to_id,
)

from src.application.dtos.db.layout import LayoutCardCreateDTO, LayoutCardDB

if TYPE_CHECKING:
    from pymongo.asynchronous.client_session import AsyncClientSession


class LayoutCardRepository(
    GetMixin[LayoutCardDB],
    AddMixin[LayoutCardCreateDTO, LayoutCardDB],
):
    async def get_by_layout_id(
        self, layout_id: str, *, session: "AsyncClientSession"
    ) -> LayoutCardDB:
        document = await self._collection.find_one(
            self._collection.layout.id == convert_to_id(layout_id),
            session=session,
            fetch_links=True,
            nesting_depths_per_field={"layout": 1},
        )
        if not document:
            raise NoContentError
        return convert_to_dto(document, LayoutCardDB)
