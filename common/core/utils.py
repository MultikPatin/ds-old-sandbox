from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import tzinfo

__all__ = ["time_now"]


def time_now(tz: "tzinfo" = UTC) -> datetime:
    return datetime.now(tz)
