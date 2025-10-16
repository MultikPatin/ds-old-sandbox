from typing import Protocol

from common.core.protocols import SessionProtocol

from src.application.dtos.db.input import InputWithTableInMatrix


class InputTemplateServiceProtocol(Protocol):
    async def generate(
        self, layout_id: str, *, session: SessionProtocol | None = None
    ) -> InputWithTableInMatrix: ...
