from typing import Any

__all__ = ["AnyDict", "AnyList", "AnyMatrix"]

type AnyDict = dict[str, Any]
type AnyList = list[Any]
type AnyMatrix = list[AnyList]
