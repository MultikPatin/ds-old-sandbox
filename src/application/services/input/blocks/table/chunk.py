from collections.abc import Generator
from typing import TYPE_CHECKING

# from abgroup_core.enums import CRUDCommandEnum
from abgroup_core.custom_types import AnyMatrix
from abgroup_core.decorators import transaction

from src.application.constants import (
    MAX_NUMBER_OF_CHUNKS,
    MAX_ROW_COUNT_PER_CHUNK,
)
from src.application.dtos.db import InputTableChunkCreateDTO

if TYPE_CHECKING:
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos.db.input import InputTableChunkDB
    from src.application.protocols import InputTableChunkRepositoryProtocol


class InputTableChunkService:
    def __init__(
        self, repo: "InputTableChunkRepositoryProtocol[SessionProtocol]"
    ) -> None:
        self._repo = repo

    @transaction
    async def add(
        self,
        values: AnyMatrix,
        *,
        session: "SessionProtocol",
        max_concurrent: int = 25,
    ) -> list["InputTableChunkDB"]:
        conditions = (
            InputTableChunkCreateDTO(values=chunk)
            for chunk in chunks_generator(values)
        )
        return await self._repo.bulk_add(
            conditions,
            session=session,
            max_concurrent=max_concurrent,
        )


#     async def rebuild_chunks(
#         self,
#         chuck_ids: list[str],
#         matrix: AnyMatrix,
#         *,
#         session: SessionProtocol | None = None,
#     ) -> list[InputTableChunkDB]:
#         results = []
#         actions = await make_actions(
#             matrix,
#             chuck_ids,
#             MAX_ROW_COUNT_PER_CHUNK,
#             MAX_NUMBER_OF_CHUNKS,
#         )
#
#         if actions.get(CRUDCommandEnum.update):
#             instances = await self._bulk_update(
#                 [
#                     InputTableChunkUpdateDTO(id=_id, values=values)
#                     for _id, values in actions[CRUDCommandEnum.update]
#                 ],
#                 session=session,
#             )
#             results.extend(instances)
#
#         if actions.get(CRUDCommandEnum.create):
#             instances = await self._bulk_add(
#                 [
#                     InputTableChunkCreateDTO(number=int(_id), values=values)
#                     for _id, values in actions[CRUDCommandEnum.create]
#                 ],
#                 session=session,
#             )
#             results.extend(instances)
#
#         if actions.get(CRUDCommandEnum.delete):
#             await self._bulk_delete(
#                 [_id for _id, _ in actions[CRUDCommandEnum.delete]],
#                 session=session,
#             )
#         return results
#
#     @transaction
#     async def _bulk_delete(
#         self,
#         ids: list[str],
#         *,
#         session: SessionProtocol | None = None,
#     ) -> list[str]:
#         # TODO: Реализовать bulk delete если возможно
#         return [await self.delete(_id, session=session) for _id in ids]
#
#     @transaction
#     async def _bulk_add(
#         self,
#         conditions: list[InputTableChunkCreateDTO],
#         *,
#         session: SessionProtocol | None = None,
#     ) -> list[InputTableChunkDB]:
#         # TODO: Реализовать bulk add если возможно
#         return [
#             await self.add(
#                 InputTableChunkCreate(number=c.number, values=c.values),
#                 session=session,
#             )
#             for c in conditions
#         ]
#
#     @transaction
#     async def _bulk_update(
#         self,
#         conditions: list[InputTableChunkUpdateDTO],
#         *,
#         session: SessionProtocol | None = None,
#     ) -> list[InputTableChunkDB]:
#         # TODO: Реализовать bulk update если возможно
#         return [
#             await self.update(
#                 c.id,
#                 InputTableChunkUpdate(values=c.values),
#                 session=session,
#             )
#             for c in conditions
#         ]
#
#     async def add(
#         self,
#         condition: InputTableChunkCreate,
#         *,
#         session: SessionProtocol | None = None,
#     ) -> InputTableChunkDB:
#         await _check_row_count(condition.values, MAX_ROW_COUNT_PER_CHUNK)
#         return await self._repo.add(condition, session=session)
#
#     async def update(
#         self,
#         _id: str,
#         condition: InputTableChunkUpdate,
#         *,
#         session: SessionProtocol | None = None,
#     ) -> InputTableChunkDB:
#         await _check_row_count(condition.values, MAX_ROW_COUNT_PER_CHUNK)
#         return await self._repo.update(_id, condition, session=session)
#
#     async def delete(
#         self,
#         _id: str,
#         *,
#         session: SessionProtocol | None = None,
#     ) -> str:
#         return await self._repo.delete(_id, session=session)
#
#
# async def make_actions(
#     matrix: AnyMatrix, ids: list[str], capacity: int, max_chunks: int
# ) -> dict[CRUDCommandEnum, list[tuple[str, AnyMatrix]]]:
#     actions: dict[CRUDCommandEnum, list[tuple[str, AnyMatrix]]] = {
#         CRUDCommandEnum.update: [],
#         CRUDCommandEnum.create: [],
#         CRUDCommandEnum.delete: [],
#     }
#
#     idx = 0
#     async for chunk in chunks_generator(matrix, capacity, max_chunks):
#         if idx <= len(ids):
#             actions[CRUDCommandEnum.update].extend([(ids[idx], chunk)])
#         else:
#             actions[CRUDCommandEnum.create].extend([(str(idx + 1), chunk)])
#         idx += 1
#
#     if idx < len(ids):
#         for i in range(idx, len(ids)):
#             actions[CRUDCommandEnum.delete].extend([(ids[i], [])])
#
#     return actions
#


def chunks_generator(matrix: AnyMatrix) -> Generator[AnyMatrix]:
    capacity = MAX_ROW_COUNT_PER_CHUNK
    max_chunks = MAX_NUMBER_OF_CHUNKS

    count = len(matrix)
    if count // capacity + 1 > max_chunks:
        # TODO: Добавить корректное исключение
        context = {
            "max_rows": count,
            "capacity": capacity,
            "max_chunks": max_chunks,
        }
        raise ValueError(context)
    offset = 0
    while count >= 0:
        yield matrix[offset : offset + capacity]
        offset += capacity
        count -= capacity


# def _check_row_count(matrix: AnyMatrix, max_rows: int) -> None:
#     if len(matrix) > max_rows:
#         # TODO: Добавить корректное исключение
#         context = {
#             "matrix_rows": len(matrix),
#             "max_rows": max_rows,
#         }
#         raise ValueError(context)
