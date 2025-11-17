from common.core.dtos import IdDTO
from pydantic import BaseModel, Field


class _ChunkForTable(IdDTO):
    id: str = Field(validation_alias="_id")


class InputTableChunksIDsProject(BaseModel):
    chunks: list[_ChunkForTable]
