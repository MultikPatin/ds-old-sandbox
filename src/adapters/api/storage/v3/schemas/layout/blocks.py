from common.fastapi.schemas import (
    BsonIDSchema,
    KeySchema,
    OptionsSchema,
    TitleSchema,
)
from pydantic import Field

from src.application.enums import LayoutMessageTypeEnum

from .cells import (
    LayoutSchemaResponse,
    LayoutStyleResponse,
    LayoutValidationResponse,
)

type SchemaLayer = list[LayoutSchemaResponse]
type ValidationLayer = list[LayoutValidationResponse | None] | None
type StyleLayer = list[LayoutStyleResponse | None] | None


class LayoutMessageResponse(BsonIDSchema, KeySchema):
    type: LayoutMessageTypeEnum = Field(
        alias="type",
        title="Type",
        description="Type of message",
    )
    lines: list[str] = Field(
        alias="lines",
        title="Lines",
        description="Lines of message",
        min_length=1,
        max_length=32,
    )
    color: str = Field(
        alias="color",
        title="Color",
        description="Color of message",
        default="#FFFFFF",
        min_length=7,
        max_length=7,
    )


class LayoutSingleResponse(BsonIDSchema, KeySchema):
    schemas: SchemaLayer = Field(
        alias="schemas",
        title="Schemas",
        description="Schema layer",
    )
    validations: ValidationLayer = Field(
        default=None,
        alias="validations",
        title="Validations",
        description="Validation layer",
    )
    styles: StyleLayer = Field(
        default=None,
        alias="styles",
        title="Styles",
        description="Style layer",
    )


class LayoutTableResponse(BsonIDSchema, KeySchema, OptionsSchema):
    schemas: list[SchemaLayer] = Field(
        alias="schemas",
        title="Schemas",
        description="Schema layer",
    )
    validations: ValidationLayer = Field(
        default=None,
        alias="validations",
        title="Validations",
        description="Validation layer",
    )
    styles: StyleLayer = Field(
        default=None,
        alias="styles",
        title="Styles",
        description="Style layer",
    )

    static: bool = Field(default=False)
    nesting: list[tuple[int, int]] | None = Field(default=None)


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
