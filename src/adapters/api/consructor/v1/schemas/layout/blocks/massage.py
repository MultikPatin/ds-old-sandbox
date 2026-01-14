from abgroup_fastapi.schemas import BsonIDSchema, KeySchema
from pydantic import Field


class LayoutMessageResponse(BsonIDSchema, KeySchema):
    is_hidden: bool = Field(
        default=True,
        alias="is_hidden",
        title="Is hidden",
        description="Is it possible to hide a message",
    )
    text: str = Field(
        min_length=1,
        max_length=512,
        alias="text",
        title="Text",
        description="Text",
    )
    color: str = Field(
        alias="color",
        title="Color",
        description="Color of message",
        default="#FFFFFF",
        min_length=7,
        max_length=7,
    )
