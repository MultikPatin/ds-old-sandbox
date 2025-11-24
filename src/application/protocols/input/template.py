from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos import InputCreateValuesDTO


class InputToolsServiceProtocol(Protocol):
    async def template(
        self, layout_key: str, *, session: "SessionProtocol"
    ) -> "InputCreateValuesDTO": ...
