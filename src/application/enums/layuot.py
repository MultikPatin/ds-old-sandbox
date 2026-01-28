from collections.abc import Iterable, Set
from enum import StrEnum, auto
from typing import Self


class LayoutBlocksEnum(StrEnum):
    singles = auto()
    tables = auto()
    messages = auto()

    @classmethod
    def fields(cls, exclude: Iterable[Self] | None = None) -> Set[Self]:
        exs = set(exclude) if exclude else set()
        return {m for m in cls if m not in exs}


class LayoutLayersEnum(StrEnum):
    schemas = auto()
    validations = auto()
    styles = auto()
    defaults = auto()

    @classmethod
    def fields(cls, exclude: Iterable[Self] | None = None) -> Set[Self]:
        exs = set(exclude) if exclude else set()
        return {m for m in cls if m not in exs}


class LayoutStyleTypeEnum(StrEnum):
    default = auto()
    range_slider = auto()
    range_datetime = auto()
    range_time = auto()
    range_date = auto()
    range = auto()
    slider = auto()
    toggle = auto()
    chips = auto()
    textarea = auto()


class LayoutDataTypeEnum(StrEnum):
    local_dropdown = auto()
    string = auto()
    bool = auto()
    float = auto()
    decimal = auto()
    date = auto()
    time = auto()
    datetime = auto()
    integer = auto()


class LayoutMessageTypeEnum(StrEnum):
    info = auto()
    error = auto()
