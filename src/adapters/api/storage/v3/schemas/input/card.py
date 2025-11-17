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
    card: list[dict[str, str]] | None = Field(default=None)
    layout: str
