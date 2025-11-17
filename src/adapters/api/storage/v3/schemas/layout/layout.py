from common.core.custom_types import AnyDict
from common.fastapi.schemas import (
    BsonIDSchema,
    CreatedSchema,
    DescriptionSchema,
    KeySchema,
    LabelSchema,
    LifeStatusSchema,
    MajorVersionSchema,
    MinorVersionSchema,
    OptionsSchema,
    UpdatedSchema,
)
from pydantic import Field

from .blocks import LayoutSingleResponse, LayoutTableResponse
from .card import LayoutCardResponse


class LayoutShortResponse(
    BsonIDSchema,
    KeySchema,
    LabelSchema,
    CreatedSchema,
    UpdatedSchema,
    DescriptionSchema,
):
    pass


class LayoutResponse(
    LayoutShortResponse,
    MinorVersionSchema,
    MajorVersionSchema,
    OptionsSchema,
    LifeStatusSchema,
):
    card: LayoutCardResponse | None = Field(
        default=None,
        alias="card",
        title="Card",
        description="Card of the layout",
    )
    sections: list[AnyDict] = Field(
        alias="sections",
        title="Sections",
        description="Sections of the layout",
    )
    singles: list[LayoutSingleResponse] | None = Field(
        default=None,
        alias="singles",
        title="Singles",
        description="Block of type 'singles' for the layout",
    )
    tables: list[LayoutTableResponse] | None = Field(
        default=None,
        alias="tables",
        title="Tables",
        description="Block of type 'tables' of the layout",
    )
