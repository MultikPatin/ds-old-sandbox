from abgroup_fastapi.schemas import (
    BsonIDSchema,
    CreatedSchema,
    LifeStatusSchema,
    OptionsSchema,
    UpdatedSchema,
)
from pydantic import Field

from .blocks import InputSingleResponse, InputTableResponse


class InputResponse(
    BsonIDSchema,
    LifeStatusSchema,
    CreatedSchema,
    UpdatedSchema,
    OptionsSchema,
):
    layout: str
    singles: list[InputSingleResponse] | None = Field(
        default=None,
        alias="singles",
        title="Singles",
        description="Block of type 'singles' for the input",
    )
    tables: list[InputTableResponse] | None = Field(
        default=None,
        alias="tables",
        title="Tables",
        description="Block of type 'tables' of the layout",
    )


class InputStatusResponse(BsonIDSchema, LifeStatusSchema):
    pass
