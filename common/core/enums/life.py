from enum import StrEnum, auto


class LifeStatusEnum(StrEnum):
    created = auto()
    draft = auto()
    published = auto()
    archived = auto()
    deleted = auto()
