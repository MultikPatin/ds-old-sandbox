from typing import Protocol

from abgroup_core.protocols import SessionProtocol

from src.application.dtos.db import LayoutCardCreateDTO, LayoutCardDB

from ._base import _RepositoryProtocol


class LayoutCardRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutCardDB,
        LayoutCardCreateDTO,
        Session,
    ],
    Protocol,
):
    async def get_by_layout_id(
        self, layout_id: str, *, session: Session
    ) -> LayoutCardDB | None: ...
