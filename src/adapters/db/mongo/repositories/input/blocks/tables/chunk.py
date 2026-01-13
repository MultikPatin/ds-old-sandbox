# from collections.abc import AsyncGenerator
# from typing import Any
#
# from collections.abc import Generator

# from abgroup_core.enums import CRUDCommandEnum
# from abgroup_core.custom_types import AnyMatrix
from common.mongo import (
    # AddMixin,
    BulkAddMixin,
    DeleteMixin,
    GetByIDsMixin,
    # UpdateMixin,
)

# from pymongo.asynchronous.client_session import AsyncClientSession
#
# from src.adapters.db.mongo.documents import (
#     InputTableChunkDocument,
# )
# from src.application.constants import (
#     MAX_NUMBER_OF_CHUNKS,
#     MAX_ROW_COUNT_PER_CHUNK,
# )
from src.application.dtos.db import (
    InputTableChunkCreateDTO,
    InputTableChunkDB,
    # InputTableChunkUpdateDTO,
)


class InputTableChunkRepository(
    GetByIDsMixin[InputTableChunkDB],
    BulkAddMixin[InputTableChunkCreateDTO, InputTableChunkDB],
    # AddMixin[InputTableChunkCreateDTO, InputTableChunkDB],
    # UpdateMixin[InputTableChunkUpdateDTO, InputTableChunkDB],
    DeleteMixin,
):
    pass


# async def _rebuild_chunks(
#     items: list[Any],
#     values: AnyMatrix,
#     *,
#     session: AsyncClientSession | None,
# ) -> list[str]:
#     new_chunks = []
#     for item in items:
#         if not isinstance(item, InputTableChunkDocument):
#             msg = "Incorrect document. Please fetch chunks before update"
#             raise TypeError(msg)
#         # TODO спорный импорт chunks_generator из сервисов
#     chunks = _chunks_generator(
#         values,
#         MAX_ROW_COUNT_PER_CHUNK,
#         MAX_NUMBER_OF_CHUNKS,
#     )
#     idx = 0
#     async for chunk in chunks:
#         if idx < len(items):
#             items[idx].values = chunk
#             await items[idx].save_changes(session=session)
#             new_chunks.append(items[idx])
#         else:
#             document = InputTableChunkDocument(
#                 number=idx,
#                 values=chunk,
#             )
#             document = await document.create(session=session)
#             new_chunks.append(document)
#         idx += 1
#     if idx < len(items):
#         for _ in range(idx, len(items)):
#             await items[idx].delete(session=session)
#     return new_chunks
#
#
# def chunks_generator(
#     matrix: AnyMatrix, capacity: int, max_chunks: int
# ) -> Generator[AnyMatrix]:
#     count = len(matrix)
#     if count // capacity + 1 > max_chunks:
#         # TODO: Добавить корректное исключение
#         context = {
#             "max_rows": count,
#             "capacity": capacity,
#             "max_chunks": max_chunks,
#         }
#         raise ValueError(context)
#     offset = 0
#     while count >= 0:
#         yield matrix[offset : offset + capacity]
#         offset += capacity
#         count -= capacity
