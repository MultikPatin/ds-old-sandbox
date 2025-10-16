from common.fastapi.schemas import (
    BsonIDSchema,
    CreatedSchema,
    LifeStatusSchema,
    OptionsSchema,
    UpdatedSchema,
)
from pydantic import BaseModel, Field

from .blocks import (
    InputSingleCreate,
    InputSingleResponse,
    InputSingleUpdateSchema,
    InputTableCreate,
    InputTableInMatrixResponse,
    InputTableResponse,
    InputTableUpdateSchema,
)


class InputStatusUpdateSchema(LifeStatusSchema):
    pass


class InputStatusResponse(BsonIDSchema, LifeStatusSchema):
    pass


class InputUpdateSchema(LifeStatusSchema, OptionsSchema):
    singles: list[InputSingleUpdateSchema] | None = Field(
        default=None,
        validation_alias="single",
        min_length=1,
    )
    tables: list[InputTableUpdateSchema] | None = Field(
        default=None,
        validation_alias="table",
        min_length=1,
    )


class InputCreate(BaseModel):
    singles: list[InputSingleCreate] | None = Field(
        default=None,
        validation_alias="single",
        min_length=1,
    )
    tables: list[InputTableCreate] | None = Field(
        default=None,
        validation_alias="table",
        min_length=1,
    )


class InputResponse(
    BsonIDSchema, LifeStatusSchema, CreatedSchema, UpdatedSchema
):
    singles: list[InputSingleResponse] | None = Field(
        default=None,
        serialization_alias="single",
    )
    tables: list[InputTableResponse] | None = Field(
        default=None,
        serialization_alias="table",
    )


class InputWithTableInMatrixResponse(
    BsonIDSchema, LifeStatusSchema, CreatedSchema, UpdatedSchema, OptionsSchema
):
    singles: list[InputSingleResponse] | None = Field(
        default=None,
        serialization_alias="single",
    )
    tables: list[InputTableInMatrixResponse] | None = Field(
        default=None,
        serialization_alias="table",
    )
