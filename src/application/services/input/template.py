from common.core.custom_types import AnyMatrix
from common.core.protocols import SessionProtocol

from src.application.dtos.db.input import (
    InputCreateDTO,
    InputSingleCreateDTO,
    InputTableCreateDTO,
    InputWithTableInMatrix,
)
from src.application.dtos.db.layout import (
    LayoutFullLinks,
    LayoutSingleFullLinks,
    LayoutTableFullLinks,
)
from src.application.protocols.repositories.layout import (
    LayoutRepositoryProtocol,
)
from src.application.protocols.services.input import InputServiceProtocol


class InputTemplateService:
    def __init__(
        self,
        layout_repo: LayoutRepositoryProtocol[SessionProtocol],
        input_service: InputServiceProtocol,
    ):
        self._layout_repo = layout_repo
        self._input_service = input_service

    async def generate(
        self, layout_id: str, *, session: SessionProtocol | None = None
    ) -> InputWithTableInMatrix:
        condition = await self._generate(layout_id, session=session)
        return await self._input_service.add(condition, session=session)

    async def _generate(
        self, layout_id: str, *, session: SessionProtocol | None = None
    ) -> InputCreateDTO:
        layout = await self._get_layout(layout_id, session=session)
        return InputCreateDTO(
            layout_id=layout_id,
            singles=await _singles(layout.singles) if layout.singles else None,
            tables=await _tables(layout.tables) if layout.tables else None,
        )

    async def _get_layout(
        self, layout_id: str, *, session: SessionProtocol | None = None
    ) -> LayoutFullLinks:
        return await self._layout_repo.get(layout_id, session=session)


async def _singles(
    items: list[LayoutSingleFullLinks],
) -> list[InputSingleCreateDTO]:
    return [
        InputSingleCreateDTO(key=item.key, values=await _s_values(item))
        for item in items
    ]


async def _s_values(single: LayoutSingleFullLinks) -> dict[str, str]:
    return {cell.key: "" for cell in single.cells}


async def _tables(
    items: list[LayoutTableFullLinks],
) -> list[InputTableCreateDTO]:
    return [
        InputTableCreateDTO(
            key=item.key,
            columns=await _t_headers(item),
            values=await _t_rows(item),
        )
        for item in items
    ]


async def _t_headers(table: LayoutTableFullLinks) -> list[str]:
    return [header.key for header in table.headers]


async def _t_rows(table: LayoutTableFullLinks) -> AnyMatrix:
    if table.rows is None:
        return []

    len_cols = len(table.headers)
    len_rows = len(table.rows)
    count = len_cols * len_rows

    matrix = [["" for _ in range(len_cols)] for _ in range(len_rows)]

    r_idx = -1
    for i in range(count):
        if i % len_cols == 0:
            r_idx += 1
            c_idx = 0
        else:
            c_idx = i % len_cols

        try:
            row = table.rows[r_idx]
            cell = row.cells[c_idx]
            if cell.default is not None:
                matrix[row.row_idx][cell.col_idx] = str(cell.default)
        except IndexError:
            pass
    return matrix
