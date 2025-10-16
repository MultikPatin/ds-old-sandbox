from common.core.protocols import SessionProtocol

from src.application.dtos.db.layout import LayoutFullLinks
from src.application.protocols.repositories.input import InputRepositoryProtocol
from src.application.protocols.repositories.layout import (
    LayoutRepositoryProtocol,
)


class LayoutService:
    def __init__(
        self,
        repo: LayoutRepositoryProtocol[SessionProtocol],
        input_repo: InputRepositoryProtocol[SessionProtocol],
    ):
        self._repo = repo
        self._input_repo = input_repo

    async def get(
        self, _id: str, *, session: SessionProtocol | None = None
    ) -> LayoutFullLinks:
        return await self._repo.get(_id, session=session)

    async def get_by_input_id(
        self, _id: str, *, session: SessionProtocol | None = None
    ) -> LayoutFullLinks:
        layout_id = await self._input_repo.get_layout_id(_id, session=session)
        return await self._repo.get(layout_id, session=session)
