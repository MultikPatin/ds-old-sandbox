from pydantic import BaseModel, Field


class MajorVersionDTO(BaseModel):
    major_version: int = Field(ge=0, default=0)


class MinorVersionDTO(BaseModel):
    minor_version: int = Field(ge=0, default=0)
