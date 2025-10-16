from enum import StrEnum, auto


class CreateUpdateEnum(StrEnum):
    created = auto()
    updated = auto()


class LifeActionTimeSortEnum(StrEnum):
    created_desc = "-created"
    created_asc = "created"
    updated_desc = "-updated"
    updated_asc = "updated"
