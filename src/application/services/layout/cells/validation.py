from typing import TYPE_CHECKING

from common.core.hashing import get_md5hash

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import (
        LayoutValidationCreateDTO,
        LayoutValidationDB,
        LayoutValidationUpdateDTO,
    )
    from src.application.protocols import LayoutValidationRepositoryProtocol


class LayoutValidationService:
    def __init__(
        self,
        repo: "LayoutValidationRepositoryProtocol[SessionProtocol]",
    ):
        self._repo = repo

    async def get(
        self, _id: str, *, session: "SessionProtocol"
    ) -> "LayoutValidationDB":
        return await self._repo.get(_id, session=session)

    async def add(
        self,
        condition: "LayoutValidationCreateDTO",
        *,
        session: "SessionProtocol",
    ) -> "LayoutValidationDB":
        condition.hash = get_md5hash(condition.model_dump())
        return await self._repo.add(condition, session=session)

    async def update(
        self,
        _id: str,
        condition: "LayoutValidationUpdateDTO",
        *,
        session: "SessionProtocol",
    ) -> "LayoutValidationDB":
        condition.hash = get_md5hash(condition.model_dump())
        return await self._repo.update(_id, condition, session=session)

    async def delete(self, _id: str, *, session: "SessionProtocol") -> str:
        return await self._repo.delete(_id, session=session)
