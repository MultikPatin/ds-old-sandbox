from common.core.decorators import transaction
from common.core.protocols import SessionProtocol

from src.application.dtos.db.input import (
    InputTableCreateDTO,
    InputTableDB,
    InputTableUpdateDTO,
)
from src.application.dtos.input import InputTableCreate, InputTableUpdate
from src.application.protocols.repositories.input import (
    InputTableRepositoryProtocol,
)
from src.application.protocols.services.input import (
    InputTableChunkServiceProtocol,
)


class InputTableService:
    def __init__(
        self,
        repo: InputTableRepositoryProtocol[SessionProtocol],
        chunk_service: InputTableChunkServiceProtocol,
    ):
        self._repo = repo
        self._chunk_service = chunk_service

    @transaction
    async def bulk_add(
        self,
        conditions: list[InputTableCreateDTO],
        *,
        session: SessionProtocol | None = None,
    ) -> list[InputTableDB]:
        # TODO: Реализовать bulk add если возможно
        return [await self.add(c, session=session) for c in conditions]

    async def bulk_add_with_return_id(
        self,
        conditions: list[InputTableCreateDTO],
        *,
        session: SessionProtocol | None = None,
    ) -> list[str]:
        instances = await self.bulk_add(conditions, session=session)
        return [i.id for i in instances]

    async def add(
        self,
        condition: InputTableCreateDTO,
        *,
        session: SessionProtocol | None = None,
    ) -> InputTableDB:
        # TODO Рассмотреть вариант возврата списка id для chunks
        chunks = await self._chunk_service.add_from_matrix(
            condition.values, session=session
        )
        return await self._repo.add(
            InputTableCreate(
                key=condition.key,
                columns=condition.columns,
                chunks=[c.id for c in chunks],
            ),
            session=session,
        )

    @transaction
    async def bulk_update(
        self,
        conditions: list[InputTableUpdateDTO],
        *,
        session: SessionProtocol | None = None,
    ) -> list[InputTableDB]:
        # TODO: Реализовать bulk update если возможно
        return [await self.update(c.id, c, session=session) for c in conditions]

    async def bulk_update_with_return_id(
        self,
        conditions: list[InputTableUpdateDTO],
        *,
        session: SessionProtocol | None = None,
    ) -> list[str]:
        instances = await self.bulk_update(conditions, session=session)
        return [i.id for i in instances]

    async def update(
        self,
        _id: str,
        condition: InputTableUpdateDTO,
        *,
        session: SessionProtocol | None = None,
    ) -> InputTableDB:
        chuck_ids = await self._repo.get_table_chunks_ids(_id, session=session)
        if chuck_ids:
            chucks = await self._chunk_service.rebuild_chunks(
                chuck_ids=chuck_ids,
                matrix=condition.values,
                session=session,
            )
        else:
            chucks = await self._chunk_service.add_from_matrix(
                condition.values, session=session
            )

        return await self._repo.update(
            _id,
            InputTableUpdate(chunks=[c.id for c in chucks]),
            session=session,
        )
