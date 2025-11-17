from pydantic import SecretStr

SETTINGS_DEFAULTS = {
    "env_file": ".env",
    "env_file_encoding": "utf-8",
    "env_nested_delimiter": "__",
    "extra": "ignore",
}

DEFAULT_HOST = "localhost"
DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = SecretStr("")
DEFAULT_DATABASE = "default-database"

DEFAULT_POSTGRES_PORT = 5432
DEFAULT_POSTGRES_ENV_PREFIX = "POSTGRES_"

DEFAULT_MONGODB_PORT = 27017
DEFAULT_MONGODB_ENV_PREFIX = "MONGODB_"

DEFAULT_MAIN_API_ENV_PREFIX = "MAIN_API_"
