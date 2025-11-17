from common.core.custom_types import AnyDict
from common.core.dtos import (
    CreatedDTO,
    DescriptionDTO,
    IdDTO,
    KeyDTO,
    LabelDTO,
    LifeStatusDTO,
    MajorVersionDTO,
    MinorVersionDTO,
    OptionsDTO,
    RefCountDTO,
    UpdatedDTO,
    UseUntilDTO,
)
from pydantic import Field

from .blocks import (
    LayoutSingleCreateDTO,
    LayoutSingleDB,
    LayoutSingleUpdateDTO,
    LayoutTableCreateDTO,
    LayoutTableDB,
    LayoutTableUpdateDTO,
)
from .card import LayoutCardCreateDTO, LayoutCardDB, LayoutCardUpdateDTO


class _LayoutShort(
    LabelDTO,
    UpdatedDTO,
    DescriptionDTO,
):
    pass


class _LayoutBase(_LayoutShort, OptionsDTO, LifeStatusDTO):
    sections: list[AnyDict]


# Update


class LayoutUpdateDTO(_LayoutBase):
    singles: list[LayoutSingleUpdateDTO] | None = Field(default=None)
    tables: list[LayoutTableUpdateDTO] | None = Field(default=None)
    card: LayoutCardUpdateDTO | None = Field(default=None)


# Base


class LayoutBase(
    _LayoutBase,
    KeyDTO,
    RefCountDTO,
    MajorVersionDTO,
    MinorVersionDTO,
    CreatedDTO,
    UseUntilDTO,
):
    sections: list[AnyDict]


class LayoutShortDTO(IdDTO, KeyDTO, _LayoutShort, CreatedDTO):
    pass


class LayoutDB(IdDTO, LayoutBase):
    pass


class LayoutWithBlocks(LayoutDB):
    singles: list[LayoutSingleDB] | None = Field(default=None)
    tables: list[LayoutTableDB] | None = Field(default=None)


class LayoutFullLinks(LayoutWithBlocks):
    card: LayoutCardDB | None = Field(default=None)


# Create


class LayoutCreateDTO(LayoutBase):
    singles: list[LayoutSingleCreateDTO] | None = Field(default=None)
    tables: list[LayoutTableCreateDTO] | None = Field(default=None)
    card: LayoutCardCreateDTO | None = Field(default=None)
