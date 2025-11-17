# from datetime import UTC, datetime
#
# from common.core.enums import LifeStatusEnum
from typing import TYPE_CHECKING

from common.core.exceptions import NoContentError
from common.mongo import (
    DeleteSoftMixin,
    GetMixin,
    KeysEnum,
    convert_to_dto,
    convert_to_id,
)

from src.adapters.db.mongo.projections import InputLayoutProjection
from src.application.dtos.db import InputFullLinks

# from src.adapters.db.mongo.documents import InputDocument
from src.application.dtos.db.input import (
    InputDB,
    # InputFullLinks,
    # InputLayoutIDProject,
    # InputUpdateDTO,
)

# from .block import rebuild_singles, rebuild_tables

if TYPE_CHECKING:
    from pymongo.asynchronous.client_session import AsyncClientSession


class InputRepository(
    GetMixin[InputDB],
    # AddMixin[InputCreate, InputDB],
    DeleteSoftMixin,
):
    async def get_full_links(
        self, _id: str, *, session: "AsyncClientSession"
    ) -> InputFullLinks:
        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
            fetch_links=True,
            nesting_depths_per_field={
                "layout": 0,
                "singles": 1,
                "tables": 1,
            },
        )
        if not document:
            raise NoContentError
        return convert_to_dto(document, InputFullLinks, is_replace_links=True)

    async def get_layout_id(
        self, _id: str, *, session: "AsyncClientSession"
    ) -> str:
        document = await self._collection.find_one(
            {KeysEnum.id: convert_to_id(_id)},
            session=session,
            projection_model=InputLayoutProjection,
        )
        if not document:
            raise NoContentError
        return document.layout

    # async def update_full_links(
    #     self,
    #     _id: str,
    #     condition: InputUpdateDTO,
    #     *,
    #     session: AsyncClientSession | None = None,
    # ) -> InputFullLinks:
    #     # TODO: Вынести глубину вложенности в отдельный конфиг возможно?
    #     specific_nesting_field = {"singles": 0, "tables": 0}
    #     if condition.singles is not None:
    #         specific_nesting_field["singles"] = 1
    #     if condition.tables is not None:
    #         specific_nesting_field["tables"] = 2
    #
    #     document = await self._get_with_links(
    #         _id,
    #         session=session,
    #         specific_nesting_field=specific_nesting_field,
    #     )
    #
    #     if document.singles is not None and condition.singles is not None:
    #         await rebuild_singles(
    #             document.singles, condition.singles, session=session
    #         )
    #     if document.tables is not None and condition.tables is not None:
    #         await rebuild_tables(
    #             document.tables, condition.tables, session=session
    #         )
    #
    #     document.status = condition.status
    #     document.updated = condition.updated
    #
    #     if condition.card is not None:
    #         document.card = condition.card
    #
    #     if condition.options is not None:
    #         document.options = condition.options
    #
    #     await document.save_changes(session=session)
    #     return convert_to_dto(document, InputFullLinks)
    #
    # async def update_status(
    #     self,
    #     _id: str,
    #     status: LifeStatusEnum,
    #     *,
    #     session: AsyncClientSession | None = None,
    # ) -> str:
    #     document = await self._get(_id, session=session)
    #     document.status = status
    #     document.updated = datetime.now(UTC)
    #     await document.save_changes(session=session)
    #     return _id
    #
    # async def _get(
    #     self, _id: str, *, session: AsyncClientSession | None = None
    # ) -> InputDocument:
    #     document = await self._collection.find_one(
    #         {KeysEnum.id: convert_to_id(_id)},
    #         session=session,
    #     )
    #     if document is None:
    #         raise NoContentError
    #     return document
    #
