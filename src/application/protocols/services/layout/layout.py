from typing import Protocol

from common.core.protocols import GetterProtocol, SessionProtocol

from src.application.dtos.db.layout import LayoutFullLinks


class LayoutServiceProtocol(
    GetterProtocol[LayoutFullLinks, SessionProtocol], Protocol
):
    async def get_by_input_id(
        self, _id: str, *, session: SessionProtocol | None = None
    ) -> LayoutFullLinks: ...
