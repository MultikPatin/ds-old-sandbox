from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos import InputCreateValuesDTO, InputWithValuesDTO
    from src.application.dtos.db import InputWithBlocks


class InputToolsServiceProtocol(Protocol):
    async def template(
        self, layout_key: str, *, session: "SessionProtocol"
    ) -> "InputCreateValuesDTO": ...
    async def set_table_values(
        self, instance: "InputWithBlocks", *, session: "SessionProtocol"
    ) -> "InputWithValuesDTO": ...
