from common.core.custom_types import AnyDict, AnyList
from pydantic import BaseModel

from src.application.dtos.db.input import (
    InputSingleBase,
    InputTableBase,
    InputTableChunkBase,
)


class InputSingleUpdate(BaseModel):
    values: AnyDict


class InputSingleCreate(InputSingleBase):
    pass


class InputTableCreate(InputTableBase):
    chunks: list[str]


class InputTableUpdate(BaseModel):
    chunks: list[str]


class InputTableChunkUpdate(BaseModel):
    values: AnyList


class InputTableChunkCreate(InputTableChunkBase):
    number: int
