from typing import Any

from common.core.dtos import (
    HashDTO,
    IdDTO,
    KeyDTO,
    LabelDTO,
    OptionsDTO,
    RequiredDTO,
)
from pydantic import Field

# TODO валидно ли использовать ReferenceDB?
from src.application.dtos.db.reference import ReferenceDB
from src.application.enums import LayoutDataType

from .style import LayoutStyleDB
from .tooltip import LayoutTooltipDB
from .validation import LayoutValidationDB


class _LayoutCell(RequiredDTO, OptionsDTO):
    default: Any = Field(default=None)
    disabled: bool = Field(default=False)


# LAYOUT REQUIRED ROW


class LayoutRequiredRowBase(OptionsDTO):
    row_idx: int = Field(ge=0, default=0)


class LayoutRequiredRowDB(IdDTO, LayoutRequiredRowBase):
    pass


class LayoutRequiredRowCreate(LayoutRequiredRowBase):
    cells: list["LayoutRequiredCellCreate"]


class LayoutRequiredRowFullLInks(IdDTO, LayoutRequiredRowBase):
    cells: list["LayoutRequiredCellFullLinks"]


# LAYOUT REQUIRED CELL


class _LayoutRequiredCellBase(_LayoutCell):
    col_idx: int = Field(ge=0, default=0)


class LayoutRequiredCellBase(HashDTO, _LayoutRequiredCellBase):
    pass


class LayoutRequiredCellCreate(_LayoutRequiredCellBase):
    tooltip: str | None = Field(default=None)


class LayoutRequiredCellDB(IdDTO, LayoutRequiredCellBase):
    pass


class LayoutRequiredCellFullLinks(IdDTO, LayoutRequiredCellBase):
    tooltip: LayoutTooltipDB | None = Field(default=None)


# LAYOUT HEADER CELL


class _LayoutHeaderCellBase(_LayoutCell, KeyDTO, LabelDTO):
    type: LayoutDataType


class LayoutHeaderCellBase(HashDTO, _LayoutHeaderCellBase):
    pass


class LayoutHeaderCellCreate(_LayoutHeaderCellBase):
    validation: str | None = Field(default=None)
    style: str | None = Field(default=None)
    tooltip: str | None = Field(default=None)
    references: list[str] | None = Field(default=None)


class LayoutHeaderCellDB(IdDTO, LayoutHeaderCellBase):
    pass


class LayoutHeaderCellFullLinks(IdDTO, LayoutHeaderCellBase):
    validation: LayoutValidationDB | None = Field(default=None)
    style: LayoutStyleDB | None = Field(default=None)
    tooltip: LayoutTooltipDB | None = Field(default=None)
    references: list[ReferenceDB] | None = Field(default=None)
