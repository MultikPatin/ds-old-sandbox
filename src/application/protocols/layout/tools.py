from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos import LayoutWithBlockLayersDTO
    from src.application.dtos.db import LayoutWithBlocks
    from src.application.protocols import LayoutFiltersProtocol


class LayoutToolsServiceProtocol(Protocol):
    async def replace_layers(
        self,
        instance: "LayoutWithBlocks",
        filters: "LayoutFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LayoutWithBlockLayersDTO": ...
    async def get_id_by_input(
        self, _id: str, *, session: "SessionProtocol"
    ) -> str: ...
