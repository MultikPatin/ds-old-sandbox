from common.core.decorators import transaction
from common.core.protocols import SessionProtocol

from src.application.dtos.db.input import (
    InputSingleCreateDTO,
    InputSingleDB,
    InputSingleUpdateDTO,
)
from src.application.dtos.input import InputSingleCreate, InputSingleUpdate
from src.application.protocols.repositories.input import (
    InputSingleRepositoryProtocol,
)


class InputSingleService:
    def __init__(self, repo: InputSingleRepositoryProtocol[SessionProtocol]):
        self._repo = repo

    @transaction
    async def bulk_add(
        self,
        conditions: list[InputSingleCreateDTO],
        *,
        session: SessionProtocol | None = None,
    ) -> list[InputSingleDB]:
        # TODO: Реализовать bulk add если возможно
        return [await self.add(c, session=session) for c in conditions]

    async def bulk_add_with_return_id(
        self,
        conditions: list[InputSingleCreateDTO],
        *,
        session: SessionProtocol | None = None,
    ) -> list[str]:
        instances = await self.bulk_add(conditions, session=session)
        return [i.id for i in instances]

    async def add(
        self,
        condition: InputSingleCreateDTO,
        *,
        session: SessionProtocol | None = None,
    ) -> InputSingleDB:
        return await self._repo.add(
            InputSingleCreate(key=condition.key, values=condition.values),
            session=session,
        )

    @transaction
    async def bulk_update(
        self,
        conditions: list[InputSingleUpdateDTO],
        *,
        session: SessionProtocol | None = None,
    ) -> list[InputSingleDB]:
        # TODO: Реализовать bulk update если возможно
        return [await self.update(c.id, c, session=session) for c in conditions]

    async def bulk_update_with_return_id(
        self,
        conditions: list[InputSingleUpdateDTO],
        *,
        session: SessionProtocol | None = None,
    ) -> list[str]:
        instances = await self.bulk_update(conditions, session=session)
        return [i.id for i in instances]

    async def update(
        self,
        _id: str,
        condition: InputSingleUpdateDTO,
        *,
        session: SessionProtocol | None = None,
    ) -> InputSingleDB:
        return await self._repo.update(
            _id,
            InputSingleUpdate(values=condition.values),
            session=session,
        )
