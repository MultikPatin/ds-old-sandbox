from typing import Protocol

from common.core.protocols import (
    AdderProtocol,
    GetterProtocol,
    SessionProtocol,
)

from src.application.dtos.db import LayoutCardCreateDTO, LayoutCardDB


class LayoutCardRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutCardDB, Session],
    AdderProtocol[LayoutCardCreateDTO, LayoutCardDB, Session],
    Protocol,
):
    async def get_by_layout_id(
        self, layout_id: str, *, session: Session
    ) -> LayoutCardDB | None: ...
