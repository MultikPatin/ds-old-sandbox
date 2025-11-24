from common.fastapi.schemas import (
    BsonIDSchema,
    KeySchema,
    LabelSchema,
    RequiredSchema,
)
from pydantic import BaseModel, Field

from src.application.enums import LayoutDataTypeEnum


class _LayoutSchema(
    LabelSchema,
    RequiredSchema,
):
    default: str | None = Field(default=None)


class _SchemaType(BaseModel):
    type: LayoutDataTypeEnum


class LayoutSchemaUpdateRequest(_LayoutSchema):
    pass


class LayoutSchemaResponse(
    BsonIDSchema,
    KeySchema,
    _LayoutSchema,
    _SchemaType,
):
    pass


class LayoutSchemaCreateRequest(
    KeySchema,
    _LayoutSchema,
    _SchemaType,
):
    pass
