from common.core.dtos import HashDTO, IdDTO, OptionsDTO
from pydantic import Field

from src.application.enums import LayoutTooltipType


class _LayoutTooltipBase(OptionsDTO):
    type: LayoutTooltipType
    header: str = Field(min_length=1, max_length=128)
    text: str | None = Field(default=None, max_length=255)


class LayoutTooltipBase(HashDTO, _LayoutTooltipBase):
    pass


class LayoutTooltipCreate(_LayoutTooltipBase):
    pass


class LayoutTooltipDB(IdDTO, LayoutTooltipBase):
    pass
