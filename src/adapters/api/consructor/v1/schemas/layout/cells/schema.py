from typing import Any

from common.fastapi.schemas import (
    BsonIDSchema,
    KeySchema,
    LabelSchema,
    RequiredSchema,
)
from pydantic import BaseModel, Field

from src.application.enums import LayoutDataType


class _LayoutSchema(
    LabelSchema,
    RequiredSchema,
):
    default: Any = Field(default=None)


class _SchemaType(BaseModel):
    type: LayoutDataType


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
