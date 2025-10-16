from pydantic import BaseModel, Field

from .base import (
    _BasePageSchema,
    _current_page_field,
    _next_page_field,
    _previous_page_field,
    _size_field,
)


class CursorParams(BaseModel):
    cursor: str | None = Field(
        default=None,
        alias="cursor",
        title="Cursor",
        description="The starting point from which "
        "the results will be searched",
    )
    size: int = _size_field()


class CursorPageResponse[Item: BaseModel](_BasePageSchema[Item]):
    current_page: str | None = _current_page_field()
    previous_page: str | None = _previous_page_field()
    next_page: str | None = _next_page_field()
