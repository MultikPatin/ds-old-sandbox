from common.core.custom_types import AnyMatrix
from common.core.dtos import IdDTO
from pydantic import BaseModel

# Update


class InputTableChunkUpdateDTO(BaseModel):
    values: AnyMatrix


# Base


class InputTableChunkBase(InputTableChunkUpdateDTO):
    pass


class InputTableChunkDB(IdDTO, InputTableChunkBase):
    pass


# Create


class InputTableChunkCreateDTO(InputTableChunkBase):
    pass
