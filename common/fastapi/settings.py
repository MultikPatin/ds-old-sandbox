from pydantic import Field
from pydantic_settings import BaseSettings

from common.core.constants import (
    API_DEFAULT_DESCRIPTION,
    API_DEFAULT_TITLE,
    DEFAULT_MAIN_API_ENV_PREFIX,
)
from common.core.settings import set_model_config


class MSettings(BaseSettings):
    model_config = set_model_config(env_prefix=DEFAULT_MAIN_API_ENV_PREFIX)

    IS_DEV_MODE: bool = Field(default=False)

    ALLOW_ORIGINS: list[str] = Field(default=["*"], min_length=1)
    ALLOW_HEADERS: list[str] = Field(default=["*"], min_length=1)
    ALLOW_METHODS: list[str] = Field(default=["*"], min_length=1)

    IS_GZIP: bool = Field(default=True)
    GZIP_MIN_SIZE: int = Field(default=500, gt=100, lt=1024 * 10)
    GZIP_COMPRESS_LEVEL: int = Field(default=6, gt=0, le=9)


class VSettings(BaseSettings):
    TITLE: str = Field(default=API_DEFAULT_TITLE, max_length=128)
    DESCRIPTION: str = Field(default=API_DEFAULT_DESCRIPTION, max_length=255)

    MAJOR_VERSION: int = Field(default=1, gt=0, le=99)
    MINOR_VERSION: int = Field(default=0, ge=0, le=99)

    IS_STATIC_DOCS: bool = Field(default=True)

    @property
    def version(self) -> str:
        return f"{self.MAJOR_VERSION}.{self.MINOR_VERSION}"

    @property
    def path(self) -> str:
        return f"/v{self.MAJOR_VERSION}"
