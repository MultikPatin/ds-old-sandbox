from abgroup_fastapi.schemas import (
    BsonIDSchema,
    KeySchema,
)
from pydantic import Field

from src.adapters.api.consructor.v1.schemas.layout.cells import (
    LayoutSchemaResponse,
    LayoutStyleResponse,
    LayoutValidationResponse,
)

type SchemaLayer = list[LayoutSchemaResponse] | None
type ValidationLayer = list[LayoutValidationResponse | None] | None
type StyleLayer = list[LayoutStyleResponse | None] | None


class LayoutSingleShortResponse(BsonIDSchema, KeySchema):
    pass


class LayoutSingleResponse(BsonIDSchema, KeySchema):
    schemas: SchemaLayer = Field(
        default=None,
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
