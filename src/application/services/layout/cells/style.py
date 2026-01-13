from typing import TYPE_CHECKING

from abgroup_core.hashing import get_md5hash

if TYPE_CHECKING:
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos.db import (
        LayoutStyleCreateDTO,
        LayoutStyleDB,
        LayoutStyleUpdateDTO,
    )
    from src.application.protocols import LayoutStyleRepositoryProtocol


class LayoutStyleService:
    def __init__(
        self,
        repo: "LayoutStyleRepositoryProtocol[SessionProtocol]",
    ) -> None:
        self._repo = repo

    async def get(
        self, _id: str, *, session: "SessionProtocol"
    ) -> "LayoutStyleDB":
        return await self._repo.get(_id, session=session)

    async def add(
        self, condition: "LayoutStyleCreateDTO", *, session: "SessionProtocol"
    ) -> "LayoutStyleDB":
        condition.hash = get_md5hash(condition.model_dump())
        return await self._repo.add(condition, session=session)

    async def update(
        self,
        _id: str,
        condition: "LayoutStyleUpdateDTO",
        *,
        session: "SessionProtocol",
    ) -> "LayoutStyleDB":
        condition.hash = get_md5hash(condition.model_dump())
        return await self._repo.update(_id, condition, session=session)

    async def delete(self, _id: str, *, session: "SessionProtocol") -> str:
        return await self._repo.delete(_id, session=session)
