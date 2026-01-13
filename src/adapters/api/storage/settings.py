from abgroup_core.settings import set_model_config
from abgroup_fastapi import MSettings

from src.application.constants import STORAGE_API_ENV_PREFIX


class Settings(MSettings):
    model_config = set_model_config(env_prefix=STORAGE_API_ENV_PREFIX)
