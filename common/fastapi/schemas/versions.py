from pydantic import BaseModel, Field, NonNegativeInt


class MajorVersionSchema(BaseModel):
    major_version: NonNegativeInt = Field(
        default=0,
        alias="major_version",
        title="Major version",
        description="Major version number",
        lt=100,
    )


class MinorVersionSchema(BaseModel):
    minor_version: NonNegativeInt = Field(
        default=0,
        alias="minor_version",
        title="Minor version",
        description="Minor version number",
        lt=100,
    )
