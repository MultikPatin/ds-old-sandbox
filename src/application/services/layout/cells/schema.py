from collections.abc import Sequence, Set
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import (
        LayoutSchemaCreateDTO,
        LayoutSchemaDB,
        LayoutSchemaUpdateDTO,
    )
    from src.application.protocols import LayoutSchemaRepositoryProtocol


class LayoutSchemaService:
    def __init__(
        self,
        repo: "LayoutSchemaRepositoryProtocol[SessionProtocol]",
    ):
        self._repo = repo

    async def get_by_ids(
        self,
        ids: Sequence[str] | Set[str],
        *,
        session: "SessionProtocol",
        batch_size: int | None = None,
        max_concurrent: int = 25,
    ) -> list["LayoutSchemaDB"]:
        return await self._repo.get_by_ids(
            ids,
            session=session,
            batch_size=batch_size,
            max_concurrent=max_concurrent,
        )

    async def get(
        self, _id: str, *, session: "SessionProtocol"
    ) -> "LayoutSchemaDB":
        return await self._repo.get(_id, session=session)

    async def add(
        self, condition: "LayoutSchemaCreateDTO", *, session: "SessionProtocol"
    ) -> "LayoutSchemaDB":
        return await self._repo.add(condition, session=session)

    async def update(
        self,
        _id: str,
        condition: "LayoutSchemaUpdateDTO",
        *,
        session: "SessionProtocol",
    ) -> "LayoutSchemaDB":
        return await self._repo.update(_id, condition, session=session)

    async def delete(self, _id: str, *, session: "SessionProtocol") -> str:
        return await self._repo.delete(_id, session=session)
