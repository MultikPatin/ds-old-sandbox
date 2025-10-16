from common.core.custom_types import AnyDict
from common.fastapi.schemas import BsonIDSchema, KeySchema, OptionsSchema
from pydantic import Field

from .cell import LayoutSHeaderCellResponse, LayoutSRequiredRowResponse


class LayoutSingleResponse(BsonIDSchema, KeySchema):
    cells: list[LayoutSHeaderCellResponse] | None = None


class LayoutTableResponse(BsonIDSchema, OptionsSchema, KeySchema):
    static: bool = Field(
        default=False,
        alias="static",
        title="Static",
        description="Determines whether the table is static, "
        "which means that the number of rows in the table does not change",
    )
    nesting: list[tuple[int, int]] | None = Field(default=None)
    level_options: AnyDict | None = Field(default=None)

    headers: list[LayoutSHeaderCellResponse] | None = None
    rows: list[LayoutSRequiredRowResponse] | None = None
