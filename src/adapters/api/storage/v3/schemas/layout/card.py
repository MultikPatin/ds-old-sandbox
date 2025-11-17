from common.fastapi.schemas import (
    BsonIDSchema,
    OptionsSchema,
    TitleSchema,
)
from pydantic import Field


class LayoutCardTitle(TitleSchema):
    path: list[str]


class LayoutCardResponse(BsonIDSchema, OptionsSchema):
    cells: list[LayoutCardTitle] | None = Field(
        default=None,
        alias="cells",
        title="Cells",
        description="cells of the layout card",
        min_length=1,
    )
