from typing import Any

from common.core.dtos import (
    CreatedDTO,
    DescriptionDTO,
    IdDTO,
    LifeStatusDTO,
    MajorVersionDTO,
    MinorVersionDTO,
    OptionsDTO,
    TitleDTO,
    UpdatedDTO,
)
from common.core.enums import LifeStatusEnum
from pydantic import Field, model_validator

from src.application import enums


class ModelBase(
    TitleDTO,
    DescriptionDTO,
    MajorVersionDTO,
    MinorVersionDTO,
    LifeStatusDTO,
    OptionsDTO,
    CreatedDTO,
    UpdatedDTO,
):
    type: enums.ModelType


class ModelDB(IdDTO, ModelBase):
    pass


class ModelWithPublishedLayoutID(ModelDB):
    layout_id: str | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def mutate_before(cls, data: Any) -> Any:
        if isinstance(data, dict):
            keys = data.get("keys", [])
            if keys:
                for key in keys:
                    layout = key.get("layout", None)
                    if layout["status"] == LifeStatusEnum.published and layout:
                        data["layout_id"] = str(layout["id"])

            return data
        return data
