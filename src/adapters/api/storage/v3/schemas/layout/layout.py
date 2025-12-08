from common.core.custom_types import AnyDict
from common.fastapi.schemas import (
    BsonIDSchema,
    CreatedSchema,
    DescriptionSchema,
    KeySchema,
    LabelSchema,
    LifeStatusSchema,
    MajorVersionSchema,
    MinorVersionSchema,
    OptionsSchema,
    UpdatedSchema,
)
from pydantic import Field

from .blocks import (
    LayoutCardResponse,
    LayoutMessageResponse,
    LayoutSingleResponse,
    LayoutTableResponse,
)

type MessageBlocks = list[LayoutMessageResponse] | None
type SingleBlocks = list[LayoutSingleResponse] | None
type TableBlocks = list[LayoutTableResponse] | None
type CardBlock = LayoutCardResponse | None


class LayoutShortResponse(
    BsonIDSchema,
    KeySchema,
    LabelSchema,
    CreatedSchema,
    UpdatedSchema,
    DescriptionSchema,
):
    pass


class LayoutResponse(
    LayoutShortResponse,
    MinorVersionSchema,
    MajorVersionSchema,
    OptionsSchema,
    LifeStatusSchema,
):
    skeleton: list[AnyDict] = Field(
        alias="skeleton",
        title="Skeleton",
        description="Skeleton of the layout",
    )

    card: CardBlock = Field(
        default=None,
        alias="card",
        title="Card",
        description="Blocks of type 'card' for the layout",
    )
    messages: MessageBlocks = Field(
        default=None,
        alias="messages",
        title="Messages",
        description="Blocks of type 'messages' for the layout",
    )
    singles: SingleBlocks = Field(
        default=None,
        alias="singles",
        title="Singles",
        description="Blocks of type 'singles' for the layout",
    )
    tables: TableBlocks = Field(
        default=None,
        alias="tables",
        title="Tables",
        description="Blocks of type 'tables' of the layout",
    )
