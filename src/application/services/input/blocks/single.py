from collections.abc import Iterable
from typing import TYPE_CHECKING

from common.core.decorators import transaction

from src.application.dtos.db import InputSingleCreateDTO

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos import InputSingleCreateValuesDTO
    from src.application.dtos.db import InputSingleDB
    from src.application.protocols import InputSingleRepositoryProtocol


class InputSingleService:
    def __init__(self, repo: "InputSingleRepositoryProtocol[SessionProtocol]"):
        self._repo = repo

    @transaction
    async def bulk_add(
        self,
        conditions: Iterable["InputSingleCreateValuesDTO"],
        *,
        session: "SessionProtocol",
        max_concurrent: int = 25,
    ) -> list["InputSingleDB"]:
        cond = (
            InputSingleCreateDTO(key=c.key, values=c.values) for c in conditions
        )
        return await self._repo.bulk_add(
            cond,
            session=session,
            max_concurrent=max_concurrent,
        )

    # async def bulk_add_with_return_id(
    #     self,
    #     conditions: list[InputSingleCreate],
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> list[str]:
    #     instances = await self.bulk_add(conditions, session=session)
    #     return [i.id for i in instances]
    #
    # async def add(
    #     self,
    #     condition: InputSingleCreate,
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> InputSingleDB:
    #     return await self._repo.add(
    #         InputSingleCreateDTO(key=condition.key, values=condition.values),
    #         session=session,
    #     )
    #
    # @transaction
    # async def bulk_update(
    #     self,
    #     conditions: list[InputSingleUpdate],
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> list[InputSingleDB]:
    #     # TODO: Реализовать bulk update если возможно
    #     return [await self.update(c.id, c, session=session) for c in conditions]
    #
    # async def bulk_update_with_return_id(
    #     self,
    #     conditions: list[InputSingleUpdate],
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> list[str]:
    #     instances = await self.bulk_update(conditions, session=session)
    #     return [i.id for i in instances]
    #
    # async def update(
    #     self,
    #     _id: str,
    #     condition: InputSingleUpdate,
    #     *,
    #     session: SessionProtocol | None = None,
    # ) -> InputSingleDB:
    #     return await self._repo.update(
    #         _id,
    #         InputSingleUpdateDTO(values=condition.values),
    #         session=session,
    #     )
