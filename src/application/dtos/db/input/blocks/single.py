from abgroup_core.custom_types import AnyDict
from abgroup_core.dtos import IdDTO, KeyDTO
from pydantic import BaseModel

# Update


class InputSingleUpdateDTO(BaseModel):
    values: AnyDict


# Base


class InputSingleBase(InputSingleUpdateDTO, KeyDTO):
    pass


class InputSingleDB(IdDTO, InputSingleBase):
    pass


# Create


class InputSingleCreateDTO(InputSingleBase):
    pass
