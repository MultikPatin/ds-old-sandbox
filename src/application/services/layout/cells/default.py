from collections.abc import Sequence, Set
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import (
        LayoutDefaultCreateDTO,
        LayoutDefaultDB,
        LayoutDefaultUpdateDTO,
    )
    from src.application.protocols import LayoutDefaultRepositoryProtocol


class LayoutDefaultService:
    def __init__(
        self,
        repo: "LayoutDefaultRepositoryProtocol[SessionProtocol]",
    ):
        self._repo = repo

    async def get_by_ids(
        self,
        ids: Sequence[str] | Set[str],
        *,
        session: "SessionProtocol",
        batch_size: int | None = None,
        max_concurrent: int = 25,
    ) -> list["LayoutDefaultDB"]:
        return await self._repo.get_by_ids(
            ids,
            session=session,
            batch_size=batch_size,
            max_concurrent=max_concurrent,
        )

    async def get(
        self, _id: str, *, session: "SessionProtocol"
    ) -> "LayoutDefaultDB":
        return await self._repo.get(_id, session=session)

    async def add(
        self, condition: "LayoutDefaultCreateDTO", *, session: "SessionProtocol"
    ) -> "LayoutDefaultDB":
        return await self._repo.add(condition, session=session)

    async def update(
        self,
        _id: str,
        condition: "LayoutDefaultUpdateDTO",
        *,
        session: "SessionProtocol",
    ) -> "LayoutDefaultDB":
        return await self._repo.update(_id, condition, session=session)

    async def delete(self, _id: str, *, session: "SessionProtocol") -> str:
        return await self._repo.delete(_id, session=session)
