from common.core.custom_types import AnyDict, AnyList
from common.core.dtos import (
    CreatedDTO,
    IdDTO,
    LifeStatusDTO,
    MajorVersionDTO,
    MinorVersionDTO,
    OptionsDTO,
    RefCountDTO,
    UpdatedDTO,
)
from pydantic import Field

from .blocks import (
    LayoutSingleCreate,
    LayoutSingleFullLinks,
    LayoutTableCreate,
    LayoutTableFullLinks,
)
from .card import LayoutCardCreate, LayoutCardDB


class LayoutBase(
    RefCountDTO,
    MajorVersionDTO,
    MinorVersionDTO,
    LifeStatusDTO,
    OptionsDTO,
    CreatedDTO,
    UpdatedDTO,
):
    sections: list[AnyDict]


class LayoutFromOldForm(LifeStatusDTO):
    version: str
    key: str
    meta_options: AnyDict | None = Field(default=None)
    input_info: AnyDict | None = Field(default=None)
    bars: AnyDict | None = Field(default=None)
    sections: AnyList = Field(min_length=1)


class LayoutCreate(LayoutBase):
    singles: list[LayoutSingleCreate] | None = Field(default=None)
    tables: list[LayoutTableCreate] | None = Field(default=None)
    card: LayoutCardCreate | None = Field(default=None)


class LayoutDB(IdDTO, LayoutBase):
    pass


class LayoutFullLinks(LayoutDB):
    singles: list[LayoutSingleFullLinks] | None = Field(default=None)
    tables: list[LayoutTableFullLinks] | None = Field(default=None)
    card: LayoutCardDB | None = Field(default=None)
