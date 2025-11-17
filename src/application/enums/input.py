from enum import StrEnum, auto


class InputBlocksEnum(StrEnum):
    singles = auto()
    tables = auto()


class InputLayersEnum(StrEnum):
    chunks = auto()
    values = auto()
