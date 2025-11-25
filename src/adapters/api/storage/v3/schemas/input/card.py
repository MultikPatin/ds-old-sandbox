from common.core.custom_types import AnyDict
from common.fastapi.schemas import (
    BsonIDSchema,
    CreatedSchema,
    LifeStatusSchema,
    OptionsSchema,
    UpdatedSchema,
)
from pydantic import Field


class InputCardResponse(
    BsonIDSchema, LifeStatusSchema, CreatedSchema, UpdatedSchema, OptionsSchema
):
    card: list[AnyDict] | None = Field(default=None)
    layout: str
