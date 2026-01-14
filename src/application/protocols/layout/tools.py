from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from abgroup_core.protocols import SessionProtocol

    from src.application.dtos import LayoutWithBlockLayersDTO
    from src.application.dtos.db import LayoutWithBlocks
    from src.application.protocols import LayersFiltersProtocol


class LayoutToolsServiceProtocol(Protocol):
    async def replace_layers(
        self,
        instance: "LayoutWithBlocks",
        filters: "LayersFiltersProtocol",
        *,
        session: "SessionProtocol",
    ) -> "LayoutWithBlockLayersDTO": ...
    async def get_id_by_input(
        self, _id: str, *, session: "SessionProtocol"
    ) -> str: ...
