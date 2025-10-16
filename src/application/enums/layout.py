from enum import StrEnum, auto


class LayoutTooltipType(StrEnum):
    info = auto()
    calculated = auto()
    sum = auto()
    division = auto()


class LayoutStyleType(StrEnum):
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


class LayoutDataType(StrEnum):
    local_dropdown = auto()
    string = auto()
    bool = auto()
    float = auto()
    date = auto()
    time = auto()
    datetime = auto()
    integer = auto()


class LayoutKeys(StrEnum):
    sections = auto()
    subsections = auto()
    blocks = auto()
    nesting_level = auto()
    sub_rows = auto()
    key = auto()
    type = auto()
    values = auto()
    rows = auto()
    name = auto()  # type: ignore
    columns = auto()
    entity = auto()
    required = auto()
    validate = auto()
