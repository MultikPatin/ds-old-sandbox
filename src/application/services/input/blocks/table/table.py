import asyncio
from collections.abc import Iterable
from typing import TYPE_CHECKING

from common.core.decorators import transaction

from src.application.dtos import InputTableWithValuesDTO
from src.application.dtos.db import InputTableCreateDTO

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos import InputTableCreateValuesDTO
    from src.application.protocols import (
        InputTableChunkServiceProtocol,
        InputTableRepositoryProtocol,
    )


class InputTableService:
    def __init__(
        self,
        repo: "InputTableRepositoryProtocol[SessionProtocol]",
        chunk_service: "InputTableChunkServiceProtocol",
    ):
        self._repo = repo
        self._chunk = chunk_service

    @transaction
    async def bulk_add(
        self,
        conditions: Iterable["InputTableCreateValuesDTO"],
        *,
        session: "SessionProtocol",
        max_concurrent: int = 25,
    ) -> list[InputTableWithValuesDTO]:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    self._chunk.add(
                        c.values,
                        session=session,
                        max_concurrent=max_concurrent,
                    )
                )
                for c in conditions
            ]

        chunks_matrix = [t.result() for t in tasks]

        cond = (
            InputTableCreateDTO(**cd.model_dump(), chunks=[c.id for c in ch])
            for cd, ch in zip(conditions, chunks_matrix, strict=True)
        )
        tables = await self._repo.bulk_add(
            cond,
            session=session,
            max_concurrent=max_concurrent,
        )

        result = []
        for t, chunks in zip(tables, chunks_matrix, strict=True):
            v = []
            for c in chunks:
                v.extend(c.values)

            result.append(InputTableWithValuesDTO(**t.model_dump(), values=v))
        return result

    # async def bulk_add_with_return_id(
    #     self,
    #     conditions: list[InputTableCreateDTO],
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> list[str]:
    #     instances = await self.bulk_add(conditions, session=session)
    #     return [i.id for i in instances]
    #
    # async def add(
    #     self,
    #     condition: InputTableCreateDTO,
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> InputTableDB:
    #     # TODO Рассмотреть вариант возврата списка id для chunks
    #     chunks = await self._chunk_service.add_from_matrix(
    #         condition.values, session=session
    #     )
    #     return await self._repo.add(
    #         InputTableCreate(
    #             key=condition.key,
    #             columns=condition.columns,
    #             chunks=[c.id for c in chunks],
    #         ),
    #         session=session,
    #     )
    #
    # @transaction
    # async def bulk_update(
    #     self,
    #     conditions: list[InputTableUpdate],
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> list[InputTableDB]:
    #     # TODO: Реализовать bulk update если возможно
    #     return [await self.update(c.id, c, session=session) for c in conditions]
    #
    # async def bulk_update_with_return_id(
    #     self,
    #     conditions: list[InputTableUpdate],
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> list[str]:
    #     instances = await self.bulk_update(conditions, session=session)
    #     return [i.id for i in instances]
    #
    # async def update(
    #     self,
    #     _id: str,
    #     condition: InputTableUpdate,
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> InputTableDB:
    #     chuck_ids = await self._repo.get_table_chunks_ids(_id, session=session)
    #     if chuck_ids:
    #         chucks = await self._chunk_service.rebuild_chunks(
    #             chuck_ids=chuck_ids,
    #             matrix=condition.values,
    #             session=session,
    #         )
    #     else:
    #         chucks = await self._chunk_service.add_from_matrix(
    #             condition.values, session=session
    #         )
    #
    #     return await self._repo.update(
    #         _id,
    #         InputTableUpdateDTO(chunks=[c.id for c in chucks]),
    #         session=session,
    #     )
