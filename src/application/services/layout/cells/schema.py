from collections.abc import Sequence, Set
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import LayoutSchemaDB
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
        max_concurrent: int = 10,
    ) -> list["LayoutSchemaDB"]:
        if isinstance(ids, Set):
            ids = list(ids)
        return await self._repo.get_by_ids(
            ids,
            session=session,
            batch_size=batch_size,
            max_concurrent=max_concurrent,
        )
