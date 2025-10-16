from pydantic import Field, MongoDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str = Field(
        default="localhost",
        min_length=1,
        max_length=255,
    )
    PORT: int = Field(default=27017, gt=0, lt=65536)
    USERNAME: str = Field(
        default="username",
        min_length=1,
        max_length=255,
    )
    PASSWORD: SecretStr = Field(
        default=SecretStr("password"),
        min_length=1,
        max_length=255,
    )
    SCHEMA: str = Field(
        default="mongodb",
        min_length=1,
        max_length=255,
    )
    DB_NAME: str = Field(
        default="db_name",
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

    @property
    def database(self) -> str:
        return self.DB_NAME
