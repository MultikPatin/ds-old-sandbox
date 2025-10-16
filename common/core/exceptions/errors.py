from typing import Any, TypeVar

from .contents import BaseErrorContent

Content = TypeVar("Content", bound=BaseErrorContent)


class AppError(Exception):
    """
    Base class for application logic errors.
    """

    def __init__(self, content: Content) -> None:
        self._content = content

    def __str__(self) -> str:
        return self._content.message

    @property
    def content(self) -> dict[str, Any]:
        return self._content.model_dump()


class NoContentError(Exception):
    """
    Raised when no content is found for the given query parameters.
    """


class LockedOperationError(Exception):
    """
    Raised when an operation is locked by service owner.
    """


class BusinessLogicError(AppError):
    """
    Raised when business logic error occurs.
    """
