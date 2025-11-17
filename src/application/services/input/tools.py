from collections.abc import Iterable
from typing import TYPE_CHECKING

from src.application.dtos.db import (
    InputCreateDTO,
    InputSingleCreateDTO,
    # InputCreateDTO,
    # InputSingleCreateDTO,
    InputTableCreateDTO,
    # InputWithTableInMatrix,
    # LayoutFullLinks,
    # LayoutSingleFullLinks,
    # LayoutTableFullLinks,
)
from src.application.dtos.filters import LayoutFilters

if TYPE_CHECKING:
    from common.core.protocols import SessionProtocol

    from src.application.dtos.layout import (
        LayoutSingleWithLayersDTO,
        LayoutTableWithLayersDTO,
    )
    from src.application.protocols import LayoutServiceProtocol


class InputToolsService:
    def __init__(
        self,
        layout_service: "LayoutServiceProtocol",
    ):
        self._layout = layout_service

    async def template(
        self, layout_key: str, *, session: "SessionProtocol"
    ) -> InputCreateDTO:
        filters = LayoutFilters(
            include_schema_layer=True,
            include_validation_layer=False,
            include_style_layer=False,
            # include_default_layer=True,
        )
        layout = await self._layout.get_with_layers_by_key(
            layout_key, filters, session=session
        )
        return InputCreateDTO(
            layout=layout.id,
            singles=self._singles(layout.singles) if layout.singles else None,
            tables=self._tables(layout.tables) if layout.tables else None,
        )

    @staticmethod
    def _singles(
        items: "Iterable[LayoutSingleWithLayersDTO]",
    ) -> list[InputSingleCreateDTO]:
        results = []
        for item in items:
            if item.schemas is None:
                msg = "For generate template, schemas must be set in layout."
                raise ValueError(msg)
            # TODO Проработать проверку и задание значений из слоя defaults
            values = {s.key: "" for s in item.schemas}
            results.append(InputSingleCreateDTO(key=item.key, values=values))
        return results

    @staticmethod
    def _tables(
        items: "Iterable[LayoutTableWithLayersDTO]",
    ) -> list[InputTableCreateDTO]:
        results = []
        for item in items:
            if item.schemas is None:
                msg = "For generate template, schemas must be set in layout."
                raise ValueError(msg)
            # TODO Проработать проверку и задание значений из слоя defaults
            # TODO Проработать создание полной таблицы при флаге static
            chunks = ["" for _ in range(len(item.schemas[0]))]
            results.append(InputTableCreateDTO(key=item.key, chunks=chunks))
        return results


# async def _t_headers(table: LayoutTableFullLinks) -> list[str]:
#     return [header.key for header in table.headers]
#
#
# async def _t_rows(table: LayoutTableFullLinks) -> AnyMatrix:
#     if table.rows is None:
#         return []
#
#     len_cols = len(table.headers)
#     len_rows = len(table.rows)
#     count = len_cols * len_rows
#
#     matrix = [["" for _ in range(len_cols)] for _ in range(len_rows)]
#
#     r_idx = -1
#     for i in range(count):
#         if i % len_cols == 0:
#             r_idx += 1
#             c_idx = 0
#         else:
#             c_idx = i % len_cols
#
#         try:
#             row = table.rows[r_idx]
#             cell = row.cells[c_idx]
#             if cell.default is not None:
#                 matrix[row.row_idx][cell.col_idx] = str(cell.default)
#         except IndexError:
#             pass
#     return matrix
