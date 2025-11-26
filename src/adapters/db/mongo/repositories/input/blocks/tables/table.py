# from collections.abc import AsyncGenerator
# from typing import Any
#
from common.mongo import BulkAddMixin

# from pymongo.asynchronous.client_session import AsyncClientSession
#
# from src.adapters.db.mongo.documents import (
#     # InputTableDocument,
# )
from src.application.dtos.db import InputTableCreateDTO, InputTableDB


class InputTableRepository(
    BulkAddMixin[InputTableCreateDTO, InputTableDB],
):
    pass


# async def rebuild_tables(
#     items: list[Any],
#     tables: list[InputTableUpdate],
#     *,
#     session: AsyncClientSession | None,
# ) -> None:
#     mapper = {table.id: table for table in tables}
#
#     for item in items:
#         if not isinstance(item, InputTableDocument):
#             msg = "Incorrect document. Please fetch tables before update"
#             raise TypeError(msg)
#         key = str(item.id)
#         if key in mapper and mapper[key].values is not None:
#             chunks = await _rebuild_chunks(
#                 item.chunks, mapper[key].values, session=session
#             )
#             item.chunks = chunks
#             await item.save_changes(session=session)
