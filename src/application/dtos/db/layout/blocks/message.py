from common.core.dtos import IdDTO, KeyDTO
from pydantic import BaseModel, Field, field_validator


class _LayoutMessageBase(BaseModel):
    is_hidden: bool = Field(default=True)
    text: str = Field(min_length=1, max_length=512)
    color: str = Field(default="#FFFFFF", min_length=7, max_length=7)

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, value: str) -> str:
        # Check for empty value
        if not value or not value.strip():
            msg = "Color value cannot be empty"
            raise ValueError(msg)

        value = value.strip()

        # Check for hash symbol
        if not value.startswith("#"):
            msg = "Color must start with '#' symbol"
            raise ValueError(msg)

        # Check length
        if len(value) not in [4, 7]:
            msg = "HEX color must be 4 (#RGB) or 7 (#RRGGBB) characters long"
            raise ValueError(msg)

        # Check characters after #
        hex_part = value[1:].upper()
        if not all(c in "0123456789ABCDEF" for c in hex_part):
            msg = "HEX color can only contain digits 0-9 and letters A-F"
            raise ValueError(msg)

        # Normalize to #RRGGBB format
        if len(value) == 4:  # #RGB format
            return f"#{hex_part[0] * 2}{hex_part[1] * 2}{hex_part[2] * 2}"

        return value.upper()


# Update


class LayoutMessageUpdateDTO(_LayoutMessageBase):
    pass


# Base


class LayoutMessageBase(KeyDTO, _LayoutMessageBase):
    pass


class LayoutMessageDB(IdDTO, LayoutMessageBase):
    pass


# Create


class LayoutMessageCreateDTO(LayoutMessageBase):
    pass
