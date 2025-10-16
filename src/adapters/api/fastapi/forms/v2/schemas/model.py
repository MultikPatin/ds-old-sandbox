from common.fastapi.schemas import (
    BsonIDSchema,
    CreatedSchema,
    DescriptionSchema,
    LifeStatusOrNoneSchema,
    OptionsSchema,
    TitleSchema,
    UpdatedSchema,
)
from common.fastapi.schemas.pagination import (
    CursorParams,
    LimitOffsetParams,
    PagesParams,
)
from pydantic import Field

from src.application.enums import ModelType


class ModelResponse(
    BsonIDSchema,
    CreatedSchema,
    UpdatedSchema,
    OptionsSchema,
    TitleSchema,
    DescriptionSchema,
):
    type: ModelType = Field(
        alias="type",
        title="Model Type",
        description="Model Type",
    )
    layout_id: str | None = Field(
        default=None,
        alias="layout_id",
        title="Layout ID",
        description="Layout ID of the current template for the model",
    )


class ModelLimitOffsetFilters(LimitOffsetParams, LifeStatusOrNoneSchema):
    pass


class ModelPagesFilters(PagesParams, LifeStatusOrNoneSchema):
    pass


class ModelCursorFilters(CursorParams, LifeStatusOrNoneSchema):
    pass
