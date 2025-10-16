from enum import StrEnum, auto


class IDTypesEnum(StrEnum):
    bson = auto()
    uuid4 = auto()
    integer = auto()
