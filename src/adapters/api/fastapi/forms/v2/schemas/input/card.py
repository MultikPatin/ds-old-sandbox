from common.fastapi.annotations import IDField
from common.fastapi.schemas import (
    BsonIDSchema,
    CreatedSchema,
    DateTimeEndSchema,
    DateTimeStartSchema,
    LifeActionSortOrNoneSchema,
    LifeActionsPeriodFieldSchema,
    LifeStatusOrNoneSchema,
    LifeStatusSchema,
    OptionsSchema,
    UpdatedSchema,
)
from common.fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import Field


class InputCardResponse(
    BsonIDSchema, LifeStatusSchema, CreatedSchema, UpdatedSchema, OptionsSchema
):
    card: list[dict[str, str]] | None = Field(default=None)


class InputCardFilters(
    DateTimeStartSchema,
    DateTimeEndSchema,
    LifeActionsPeriodFieldSchema,
    LifeStatusOrNoneSchema,
    LifeActionSortOrNoneSchema,
):
    model_id: str = IDField(
        alias="model_id", description_prefix="Model ID <br><br>"
    )


class InputCardLimitOffsetFilters(LimitOffsetParams, InputCardFilters):
    pass


class InputCardPagesFilters(PagesParams, InputCardFilters):
    pass


class InputCardCursorFilters(CursorParams, InputCardFilters):
    pass
