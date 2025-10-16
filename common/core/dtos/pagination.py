from collections.abc import Sequence

from pydantic import BaseModel, Field

# PAGINATION PARAMS


class PagesParamsDTO(BaseModel):
    number: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=1, le=100)


class LimitOffsetParamsDTO(BaseModel):
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class CursorParamsDTO(BaseModel):
    cursor: str | None = Field(default=None)
    size: int = Field(default=50, ge=1, le=100)


# PAGINATION RESULTS


class BasePage[Item: BaseModel](BaseModel):
    items: Sequence[Item]
    total: int | None = Field(default=None)


class PagesPageDTO[Item: BaseModel](BasePage[Item]):
    current_page: int | None = Field(default=None)
    previous_page: int | None = Field(default=None)
    next_page: int | None = Field(default=None)


class LimitOffsetPageDTO[Item: BaseModel](BasePage[Item]):
    limit: int | None = Field(ge=1)
    offset: int | None = Field(ge=0)


class CursorPageDTO[Item: BaseModel](BasePage[Item]):
    current_page: str | None = Field(default=None)
    previous_page: str | None = Field(default=None)
    next_page: str | None = Field(default=None)
