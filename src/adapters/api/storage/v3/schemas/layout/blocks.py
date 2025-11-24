from common.fastapi.schemas import (
    BsonIDSchema,
    KeySchema,
    OptionsSchema,
)
from pydantic import Field

from .cells import (
    LayoutSchemaResponse,
    LayoutStyleResponse,
    LayoutValidationResponse,
)


class LayoutSingleResponse(BsonIDSchema, KeySchema):
    schemas: list[LayoutSchemaResponse] | None = Field(
        default=None,
        alias="schemas",
        title="Schemas",
        description="Schema layer",
    )
    validations: list[LayoutValidationResponse] | None = Field(
        default=None,
        alias="validations",
        title="Validations",
        description="Validation layer",
    )
    styles: list[LayoutStyleResponse] | None = Field(
        default=None,
        alias="styles",
        title="Styles",
        description="Style layer",
    )


class LayoutTableResponse(BsonIDSchema, KeySchema, OptionsSchema):
    static: bool = Field(default=False)
    nesting: list[tuple[int, int]] | None = Field(default=None)
    schemas: list[list[LayoutSchemaResponse]] | None = Field(
        default=None,
        alias="schemas",
        title="Schemas",
        description="Schema layer",
    )
    validations: list[list[LayoutValidationResponse]] | None = Field(
        default=None,
        alias="validations",
        title="Validations",
        description="Validation layer",
    )
    styles: list[list[LayoutStyleResponse]] | None = Field(
        default=None,
        alias="styles",
        title="Styles",
        description="Style layer",
    )
