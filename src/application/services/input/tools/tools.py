from typing import TYPE_CHECKING

from src.application.dtos.filters import LayoutFilters

from .template import generate_template

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos import InputCreateValuesDTO
    from src.application.protocols import LayoutServiceProtocol


class InputToolsService:
    def __init__(
        self,
        layout_service: "LayoutServiceProtocol",
    ):
        self._layout = layout_service

    async def template(
        self, layout_key: str, *, session: "SessionProtocol"
    ) -> "InputCreateValuesDTO":
        filters = LayoutFilters(
            include_schema_layer=True,
            include_validation_layer=False,
            include_style_layer=False,
            include_default_layer=True,
        )
        layout = await self._layout.get_with_layers_by_key(
            layout_key, filters, session=session
        )
        return generate_template(layout)
