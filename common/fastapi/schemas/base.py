from pydantic import BaseModel, Field

from common.core.custom_types import AnyDict


class OptionsSchema(BaseModel):
    options: AnyDict | None = Field(
        default=None,
        alias="options",
        title="Options",
        description="Used to pass additional options to the instance",
    )


class KeySchema(BaseModel):
    key: str = Field(
        min_length=1,
        max_length=32,
        alias="key",
        title="Key",
        description="Key used to identify the instance",
    )


class ValueSchema(BaseModel):
    value: str = Field(
        min_length=1,
        max_length=64,
        alias="value",
        title="Value",
        description="Used to store the value",
    )


class LabelSchema(BaseModel):
    label: str = Field(
        min_length=1,
        max_length=128,
        alias="label",
        title="Label",
        description="Label of the instance",
    )


class TitleSchema(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=128,
        alias="title",
        title="Title",
        description="Title of the instance",
    )


class DescriptionSchema(BaseModel):
    description: str | None = Field(
        default=None,
        alias="description",
        title="Description",
        description="Description of the instance",
    )


class RequiredSchema(BaseModel):
    required: bool = Field(
        alias="required",
        title="Required",
        description="Required flag",
    )
