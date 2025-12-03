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

type Schemas = list[LayoutSchemaResponse]
type Validations = list[LayoutValidationResponse | None] | None
type Styles = list[LayoutStyleResponse | None] | None


class LayoutSingleResponse(BsonIDSchema, KeySchema):
    schemas: Schemas = Field(
        alias="schemas",
        title="Schemas",
        description="Schema layer",
    )
    validations: Validations = Field(
        default=None,
        alias="validations",
        title="Validations",
        description="Validation layer",
    )
    styles: Styles = Field(
        default=None,
        alias="styles",
        title="Styles",
        description="Style layer",
    )


class LayoutTableResponse(BsonIDSchema, KeySchema, OptionsSchema):
    schemas: list[Schemas] = Field(
        alias="schemas",
        title="Schemas",
        description="Schema layer",
    )
    validations: Validations = Field(
        default=None,
        alias="validations",
        title="Validations",
        description="Validation layer",
    )
    styles: Styles = Field(
        default=None,
        alias="styles",
        title="Styles",
        description="Style layer",
    )

    static: bool = Field(default=False)
    nesting: list[tuple[int, int]] | None = Field(default=None)
