from common.core.custom_types import AnyDict
from common.core.dtos import IdDTO, KeyDTO, OptionsDTO
from pydantic import Field

from .cells import (
    LayoutHeaderCellCreate,
    LayoutHeaderCellFullLinks,
    LayoutRequiredRowCreate,
    LayoutRequiredRowFullLInks,
)


class LayoutTableBase(KeyDTO, OptionsDTO):
    static: bool = Field(default=False)
    nesting: list[tuple[int, int]] | None = Field(default=None)
    level_options: AnyDict | None = Field(default=None)


class LayoutTableCreate(LayoutTableBase):
    headers: list[LayoutHeaderCellCreate]
    rows: list[LayoutRequiredRowCreate] | None = Field(default=None)


class LayoutTableDB(IdDTO, LayoutTableBase):
    pass


class LayoutTableFullLinks(LayoutTableDB):
    headers: list[LayoutHeaderCellFullLinks]
    rows: list[LayoutRequiredRowFullLInks] | None = Field(default=None)
