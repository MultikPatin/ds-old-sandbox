from typing import TYPE_CHECKING

from src.application.dtos import InputWithValuesDTO
from src.application.dtos.filters import LayoutFilters

from .replacer import get_chunk_ids, replace_layers
from .template import generate_template

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos import InputCreateValuesDTO
    from src.application.dtos.db import InputWithBlocks
    from src.application.protocols import (
        InputTableChunkRepositoryProtocol,
        LayoutServiceProtocol,
    )


class InputToolsService:
    def __init__(
        self,
        *,
        layout_service: "LayoutServiceProtocol",
        table_chunk_repo: "InputTableChunkRepositoryProtocol[SessionProtocol]",
    ):
        self._layout = layout_service
        self._chunk_repo = table_chunk_repo

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

    async def set_table_values(
        self,
        instance: "InputWithBlocks",
        *,
        session: "SessionProtocol",
    ) -> InputWithValuesDTO:
        ids = get_chunk_ids(instance)
        results = await self._chunk_repo.get_by_ids(ids, session=session)
        changes = {r.id: r.model_dump() for r in results}
        # TODO Реализовать работу с отдачей чанка по номеру
        #   добавить фильтрацию к запросу
        #   добавить параметры в фильтр (chunk_number, total_chunks)
        #   первично или при пустых значениях отдавать первый чанк
        #   преобразование вести в методе _set_values
        return InputWithValuesDTO(**replace_layers(instance, changes))
