from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from beanie.odm.enums import SortDirection

__all__ = ["Sort"]

type Sort = None | str | list[tuple[str, SortDirection]]
