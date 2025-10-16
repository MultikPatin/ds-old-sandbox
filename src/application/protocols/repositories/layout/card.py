from typing import Protocol

from common.core.protocols import (
    AdderProtocol,
    GetterProtocol,
    SessionProtocol,
)

from src.application.dtos.db.layout import LayoutCardCreate, LayoutCardDB


class LayoutCardRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutCardDB, Session],
    AdderProtocol[LayoutCardCreate, LayoutCardDB, Session],
    Protocol,
):
    async def get_by_layout_id(
        self, layout_id: str, *, session: Session | None = None
    ) -> LayoutCardDB | None: ...
