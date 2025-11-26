from collections.abc import Sequence
from enum import StrEnum, auto
from typing import Self


class LifeStatusEnum(StrEnum):
    created = auto()
    draft = auto()
    published = auto()
    archived = auto()
    deleted = auto()

    @classmethod
    def values(cls, exclude: Sequence[Self] | None = None) -> list[Self]:
        exs = set(exclude) if exclude else set()
        return [m for m in cls if m not in exs]
