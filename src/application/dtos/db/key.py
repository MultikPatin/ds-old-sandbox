from common.core.dtos import IdDTO, KeyDTO
from pydantic import BaseModel


class KeyBase(KeyDTO):
    pass


class KeyDB(IdDTO, KeyBase):
    pass


class KeyLinks(BaseModel):
    model: str
    layout: str
