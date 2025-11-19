from common.core.dtos import IdDTO, KeyDTO
from pydantic import BaseModel

# Update


class InputTableUpdateDTO(BaseModel):
    chunks: list[str]


# Base


class InputTableBase(InputTableUpdateDTO, KeyDTO):
    pass


class InputTableDB(IdDTO, InputTableBase):
    pass


# Create


class InputTableCreateDTO(InputTableBase):
    pass
