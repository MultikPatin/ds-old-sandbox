from common.core.dtos import HashDTO, HashOrNoneDTO, IdDTO, OptionsDTO
from pydantic import Field

from src.application.enums import LayoutStyleTypeEnum


class _LayoutStyleBase(OptionsDTO):
    type: LayoutStyleTypeEnum = Field(default=LayoutStyleTypeEnum.default)
    width: int | None = Field(default=None)
    decimal_places: int | None = Field(default=None)
    postfix: str | None = Field(default=None)
    prefix: str | None = Field(default=None)

    def is_empty(self) -> bool:
        if self.type == LayoutStyleTypeEnum.default:
            return not any(self.model_dump(exclude={"type"}).values())
        return False


# Update


class LayoutStyleUpdateDTO(HashOrNoneDTO, _LayoutStyleBase):
    pass


# Base


class LayoutStyleBase(HashDTO, _LayoutStyleBase):
    pass


class LayoutStyleDB(IdDTO, LayoutStyleBase):
    pass


# Create


class LayoutStyleCreateDTO(HashOrNoneDTO, _LayoutStyleBase):
    pass
