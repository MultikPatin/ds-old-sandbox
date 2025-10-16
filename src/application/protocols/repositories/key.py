from typing import Protocol

from common.core.protocols import SessionProtocol

from src.application.dtos.db.key import KeyLinks


class KeyRepositoryProtocol[Session: SessionProtocol](Protocol):
    async def get_by_model_id(
        self, model_id: str, *, session: Session | None = None
    ) -> list[KeyLinks]: ...
    async def get_by_layout_id(
        self, layout_id: str, *, session: Session | None = None
    ) -> KeyLinks: ...
