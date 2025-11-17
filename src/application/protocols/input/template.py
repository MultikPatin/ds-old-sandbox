from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.db import InputCreateDTO


class InputToolsServiceProtocol(Protocol):
    async def template(
        self, layout_key: str, *, session: "SessionProtocol"
    ) -> "InputCreateDTO": ...
