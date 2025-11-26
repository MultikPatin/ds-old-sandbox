# from collections.abc import AsyncGenerator
# from typing import Any

from common.mongo import BulkAddMixin

# from pymongo.asynchronous.client_session import AsyncClientSession
#
# from src.adapters.db.mongo.documents import (
#     # InputSingleDocument,
# )
from src.application.dtos.db import InputSingleCreateDTO, InputSingleDB


class InputSingleRepository(
    BulkAddMixin[InputSingleCreateDTO, InputSingleDB],
):
    pass


# async def rebuild_singles(
#     items: list[Any],
#     singles: list[InputSingleUpdate],
#     *,
#     session: AsyncClientSession | None,
# ) -> None:
#     mapper = {single.id: single for single in singles}
#
#     for item in items:
#         if not isinstance(item, InputSingleDocument):
#             msg = "Incorrect document. Please fetch singles before update"
#             raise TypeError(msg)
#         key = str(item.id)
#         if key in mapper:
#             item.values = mapper[key].values
#             await item.save_changes(session=session)
