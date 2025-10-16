from pydantic import BaseModel, Field

from .base import _BasePageSchema


class LimitOffsetParams(BaseModel):
    offset: int = Field(
        alias="offset",
        title="Offset",
        description="Offset to the first element",
        default=0,
        ge=0,
    )
    limit: int = Field(
        alias="limit",
        title="Limit",
        description="Number of elements",
        default=50,
        ge=1,
        le=100,
    )


class LimitOffsetPageResponse[Item: BaseModel](_BasePageSchema[Item]):
    limit: int | None = Field(
        ge=1,
        alias="limit",
        title="Limit",
        description="Number of elements",
    )
    offset: int | None = Field(
        ge=0,
        alias="offset",
        title="Offset",
        description="Offset to the first element",
    )
