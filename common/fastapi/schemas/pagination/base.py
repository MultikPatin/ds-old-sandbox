from collections.abc import Sequence
from functools import partial

from pydantic import BaseModel, Field


class _BasePageSchema[Item: BaseModel](BaseModel):
    items: Sequence[Item] = Field(
        alias="items",
        title="Items",
        description="Founded instances",
        min_length=1,
    )
    total: int | None = Field(
        default=None,
        alias="total",
        title="Total",
        description="Total count of instances",
    )


_size_field = partial(
    Field,
    default=50,
    alias="size",
    title="Size",
    description="Number of elements",
    ge=1,
    le=100,
)
_current_page_field = partial(
    Field,
    default=None,
    alias="current_page",
    title="Current page",
    description="Current page number",
)
_previous_page_field = partial(
    Field,
    default=None,
    alias="previous_page",
    title="Previous page",
    description="Previous page number",
)
_next_page_field = partial(
    Field,
    default=None,
    alias="next_page",
    title="Next page",
    description="Next page number",
)
