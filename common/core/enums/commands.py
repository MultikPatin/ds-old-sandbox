from enum import StrEnum, auto


class CRUDCommandEnum(StrEnum):
    create = auto()
    read = auto()
    update = auto()
    delete = auto()
