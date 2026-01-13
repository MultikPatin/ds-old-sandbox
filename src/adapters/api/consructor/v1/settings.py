from abgroup_core.settings import set_model_config
from abgroup_fastapi import VSettings

from src.application.constants import (
    CONSTRUCTOR_API_ENV_PREFIX,
    get_versioned_prefix,
)


class Settings(VSettings):
    model_config = set_model_config(
        env_prefix=get_versioned_prefix(
            prefix=CONSTRUCTOR_API_ENV_PREFIX, version=1
        )
    )
