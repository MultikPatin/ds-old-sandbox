from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from abgroup_core.protocols import SessionProtocol

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
    ) -> None:
        self._repo = repo

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
