from pydantic import BaseModel, Field

from .base import (
    _BasePageSchema,
    _current_page_field,
    _next_page_field,
    _previous_page_field,
    _size_field,
)


class PagesParams(BaseModel):
    number: int = Field(
        alias="number",
        title="Number",
        description="Number of page",
        default=1,
        ge=1,
    )
    size: int = _size_field()


class PagesPageResponse[Item: BaseModel](_BasePageSchema[Item]):
    current_page: int | None = _current_page_field()
    previous_page: int | None = _previous_page_field()
    next_page: int | None = _next_page_field()
