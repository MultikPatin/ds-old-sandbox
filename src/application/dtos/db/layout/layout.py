from abgroup_core.custom_types import AnyDict
from abgroup_core.dtos import (
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
    LayoutCardCreateDTO,
    LayoutCardDB,
    LayoutCardUpdateDTO,
    LayoutMessageCreateDTO,
    LayoutMessageDB,
    LayoutMessageUpdateDTO,
    LayoutSingleCreateDTO,
    LayoutSingleDB,
    LayoutSingleUpdateDTO,
    LayoutTableCreateDTO,
    LayoutTableDB,
    LayoutTableUpdateDTO,
)


class _LayoutShort(LabelDTO, UpdatedDTO, DescriptionDTO):
    pass


class _LayoutBase(_LayoutShort, OptionsDTO, LifeStatusDTO):
    skeleton: list[AnyDict]


# Update


class LayoutUpdateDTO(_LayoutBase):
    card: LayoutCardUpdateDTO | None = Field(default=None)

    singles: list[LayoutSingleUpdateDTO] | None = Field(default=None)
    tables: list[LayoutTableUpdateDTO] | None = Field(default=None)
    messages: list[LayoutMessageUpdateDTO] | None = Field(default=None)


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
    pass


class LayoutShortDTO(IdDTO, KeyDTO, _LayoutShort, CreatedDTO):
    pass


class LayoutDB(IdDTO, LayoutBase):
    pass


class LayoutWithBlocks(LayoutDB):
    singles: list[LayoutSingleDB] | None = Field(default=None)
    tables: list[LayoutTableDB] | None = Field(default=None)
    messages: list[LayoutMessageDB] | None = Field(default=None)


class LayoutFullLinks(LayoutWithBlocks):
    card: LayoutCardDB | None = Field(default=None)


# Create


class LayoutCreateDTO(LayoutBase):
    card: LayoutCardCreateDTO | None = Field(default=None)

    singles: list[LayoutSingleCreateDTO] | None = Field(default=None)
    tables: list[LayoutTableCreateDTO] | None = Field(default=None)
    messages: list[LayoutMessageCreateDTO] | None = Field(default=None)
