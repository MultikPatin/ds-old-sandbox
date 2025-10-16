from common.core.custom_types import AnyDict
from common.core.dtos import IdDTO, KeyDTO


class InputSingleCreateDTO(KeyDTO):
    values: AnyDict


class InputSingleUpdateDTO(IdDTO):
    values: AnyDict


class InputSingleBase(KeyDTO):
    values: AnyDict


class InputSingleDB(IdDTO, InputSingleBase):
    pass
