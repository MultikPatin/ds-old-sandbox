from pydantic import Field
from pydantic_settings import BaseSettings

from common.core.constants import (
    API_DEFAULT_DESCRIPTION,
    API_DEFAULT_TITLE,
    API_DEFAULT_VERSION,
)


class Settings(BaseSettings):
    TITLE: str = Field(default=API_DEFAULT_TITLE)
    DESCRIPTION: str = Field(default=API_DEFAULT_DESCRIPTION)
    VERSION: str = Field(default=API_DEFAULT_VERSION)

    PATH: str = Field(default="")

    IS_STATIC_DOCS: bool = Field(default=True)
