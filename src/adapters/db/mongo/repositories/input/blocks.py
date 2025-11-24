# from collections.abc import AsyncGenerator
# from typing import Any
#
# from common.core.custom_types import AnyMatrix
from common.mongo import (
    BulkAddMixin,
    # AddMixin,
    DeleteMixin,
    GetByIDsMixin,
)

# from pymongo.asynchronous.client_session import AsyncClientSession
#
# from src.adapters.db.mongo.documents import (
#     # InputSingleDocument,
#     InputTableChunkDocument,
#     # InputTableDocument,
# )
# from src.application.constants import (
#     MAX_NUMBER_OF_CHUNKS,
#     MAX_ROW_COUNT_PER_CHUNK,
# )
from src.application.dtos.db import (
    InputSingleCreateDTO,
    InputTableChunkCreateDTO,
    InputTableCreateDTO,
    InputTableDB,
)
from src.application.dtos.db.input import (
    InputSingleDB,
    InputTableChunkDB,
)


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


class InputTableRepository(
    BulkAddMixin[InputTableCreateDTO, InputTableDB],
):
    pass
    # async def get_table_chunks_ids(
    #     self, _id: str, *, session: AsyncClientSession | None = None
    # ) -> list[str]:
    #     # TODO: Необходимо ли возвращать dtos.repository.InputTable
    #     document = await self._collection.find_one(
    #         {KeysEnum.id: convert_to_id(_id)},
    #         session=session,
    #         projection_model=InputTableChunksIDsProject,
    #         fetch_links=True,
    #         nesting_depths_per_field={"chunks": 1},
    #     )
    #     if not document:
    #         raise NoContentError
    #     return [chunk.id for chunk in document.chunks]


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


class InputTableChunkRepository(
    GetByIDsMixin[InputTableChunkDB],
    BulkAddMixin[InputTableChunkCreateDTO, InputTableChunkDB],
    # AddMixin[InputTableChunkCreate, InputTableChunkDB],
    # UpdateMixin[InputTableChunkUpdate, InputTableChunkDB],
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
# async def _chunks_generator(
#     matrix: AnyMatrix, chunk_capacity: int, max_chunks: int
# ) -> AsyncGenerator[AnyMatrix]:
#     count = len(matrix)
#     if count // chunk_capacity + 1 > max_chunks:
#         # TODO: Добавить корректное исключение
#         context = {
#             "matrix_rows": count,
#             "chunk_capacity": chunk_capacity,
#             "max_chunks": max_chunks,
#         }
#         raise ValueError(context)
#     offset = 0
#     while count >= 0:
#         yield matrix[offset : offset + chunk_capacity]
#         offset += chunk_capacity
#         count -= chunk_capacity
