from typing import Any, TypeVar

__all__ = ["AnyDict", "AnyList", "AnyMatrix", "SessionType"]

type AnyDict = dict[str, Any]
type AnyList = list[Any]
type AnyMatrix = list[AnyList]

SessionType = TypeVar("SessionType")
