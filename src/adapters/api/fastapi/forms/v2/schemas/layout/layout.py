from common.core.custom_types import AnyDict
from common.fastapi.schemas import (
    BsonIDSchema,
    CreatedSchema,
    MajorVersionSchema,
    MinorVersionSchema,
    OptionsSchema,
    UpdatedSchema,
)
from pydantic import Field

from .blocks import LayoutSingleResponse, LayoutTableResponse
from .card import LayoutCardResponse


class LayoutResponse(
    BsonIDSchema,
    OptionsSchema,
    MinorVersionSchema,
    MajorVersionSchema,
    CreatedSchema,
    UpdatedSchema,
):
    card: LayoutCardResponse | None = Field(
        default=None,
        alias="card",
        title="Card",
        description="Card of the layout",
    )
    # Layout tree
    sections: list[AnyDict] = Field(
        alias="sections",
        title="Sections",
        description="Sections of the layout",
    )
    # Blocks of the layout
    singles: list[LayoutSingleResponse] | None = Field(
        default=None,
        alias="singles",
        title="Singles",
        description="Block of type 'single' for the layout",
    )
    tables: list[LayoutTableResponse] | None = Field(
        default=None,
        alias="tables",
        title="Tables",
        description="Block of type 'table' of the layout",
    )
