from common.core.enums import LifeStatusEnum
from pydantic import Field

from src.application.dtos.db.input import InputBase


class InputCreate(InputBase):
    layout: str
    status: LifeStatusEnum = Field(default=LifeStatusEnum.created)

    singles: list[str] | None = Field(default=None)
    tables: list[str] | None = Field(default=None)
