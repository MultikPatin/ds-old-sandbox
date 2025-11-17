from collections.abc import Sequence, Set
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import LayoutValidationDB
    from src.application.protocols import LayoutValidationRepositoryProtocol


class LayoutValidationService:
    def __init__(
        self,
        repo: "LayoutValidationRepositoryProtocol[SessionProtocol]",
    ):
        self._repo = repo

    async def get_by_ids(
        self,
        ids: Sequence[str] | Set[str],
        *,
        session: "SessionProtocol",
        batch_size: int | None = None,
        max_concurrent: int = 10,
    ) -> list["LayoutValidationDB"]:
        if isinstance(ids, Set):
            ids = list(ids)
        return await self._repo.get_by_ids(
            ids,
            session=session,
            batch_size=batch_size,
            max_concurrent=max_concurrent,
        )
