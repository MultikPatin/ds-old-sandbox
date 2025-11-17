from pydantic import Field, MongoDsn, SecretStr
from pydantic_settings import BaseSettings

from common.core.constants import (
    DEFAULT_DATABASE,
    DEFAULT_HOST,
    DEFAULT_MONGODB_ENV_PREFIX,
    DEFAULT_MONGODB_PORT,
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
)
from common.core.settings import set_model_config


class Settings(BaseSettings):
    model_config = set_model_config(env_prefix=DEFAULT_MONGODB_ENV_PREFIX)

    HOST: str = Field(
        default=DEFAULT_HOST,
        min_length=1,
        max_length=255,
    )
    PORT: int = Field(default=DEFAULT_MONGODB_PORT, gt=0, lt=65536)
    USERNAME: str = Field(
        default=DEFAULT_USERNAME,
        max_length=255,
    )
    PASSWORD: SecretStr = Field(
        default=DEFAULT_PASSWORD,
        max_length=255,
    )
    SCHEMA: str = Field(
        default="mongodb",
        min_length=1,
        max_length=255,
    )
    DATABASE: str = Field(
        default=DEFAULT_DATABASE,
        min_length=1,
        max_length=255,
    )

    @property
    def dsn(self) -> MongoDsn:
        return MongoDsn.build(
            host=self.HOST,
            port=self.PORT,
            scheme=self.SCHEMA,
            username=self.USERNAME,
            password=self.PASSWORD.get_secret_value(),
        )
