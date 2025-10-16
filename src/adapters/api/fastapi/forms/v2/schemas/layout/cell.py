from typing import Any

from common.core.custom_types import AnyDict
from common.fastapi.schemas import BsonIDSchema, KeySchema, OptionsSchema
from pydantic import Field

from src.application.enums import (
    LayoutDataType,
    LayoutStyleType,
    LayoutTooltipType,
)

from .reference import LayoutReferencesResponse


class LayoutTooltipResponse(BsonIDSchema):
    type: LayoutTooltipType
    header: str
    text: str


class LayoutStyleResponse(BsonIDSchema, OptionsSchema):
    type: LayoutStyleType
    dimension: AnyDict | None = Field(default=None)
    decimal_places: int | None = Field(default=None)
    postfix: str | None = Field(default=None)
    prefix: str | None = Field(default=None)


class LayoutValidationResponse(BsonIDSchema, OptionsSchema):
    gt: int | None = Field(default=None)
    ge: int | None = Field(default=None)
    lt: int | None = Field(default=None)
    le: int | None = Field(default=None)
    max_digits: int | None = Field(default=None)
    decimal_places: int | None = Field(default=None)

    min_length: int | None = Field(default=None)
    max_length: int | None = Field(default=None)


class _LayoutCell(BsonIDSchema):
    required: bool = Field(default=False)
    default: Any = Field(default=None)
    disabled: bool = Field(default=False)


class LayoutSRequiredRowResponse(BsonIDSchema, OptionsSchema):
    row_idx: int = Field(ge=0, default=0)
    cells: list["LayoutSRequiredCellResponse"]


class LayoutSRequiredCellResponse(_LayoutCell, OptionsSchema):
    col_idx: int = Field(ge=0, default=0)
    tooltip: LayoutTooltipResponse | None = Field(default=None)


class LayoutSHeaderCellResponse(_LayoutCell, KeySchema, OptionsSchema):
    type: LayoutDataType
    validation: LayoutValidationResponse | None = Field(default=None)
    style: LayoutStyleResponse | None = Field(default=None)
    tooltip: LayoutTooltipResponse | None = Field(default=None)
    references: list["LayoutReferencesResponse"] | None = Field(default=None)
