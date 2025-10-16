from common.core.custom_types import AnyList, AnyMatrix
from common.core.dtos import IdDTO, KeyDTO
from pydantic import BaseModel, Field


class InputTableCreateDTO(KeyDTO):
    columns: list[str]
    values: AnyMatrix


class InputTableUpdateDTO(IdDTO):
    values: AnyMatrix


class InputTableBase(KeyDTO):
    columns: list[str]


class InputTableDB(IdDTO, InputTableBase):
    pass


class InputTableInMatrix(InputTableDB):
    values: AnyMatrix


class InputTableFullLinks(IdDTO, InputTableBase):
    chunks: list["InputTableChunkDB"]


# Chunks


class InputTableChunkUpdateDTO(IdDTO):
    values: AnyMatrix


class InputTableChunkCreateDTO(BaseModel):
    number: int = Field(gt=0)
    values: AnyList


class InputTableChunkBase(BaseModel):
    number: int
    values: AnyList


class InputTableChunkDB(IdDTO, InputTableChunkBase):
    pass
