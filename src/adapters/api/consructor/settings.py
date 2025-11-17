from common.core.settings import set_model_config
from common.fastapi import MSettings

from src.application.constants import CONSTRUCTOR_API_ENV_PREFIX


class Settings(MSettings):
    model_config = set_model_config(env_prefix=CONSTRUCTOR_API_ENV_PREFIX)
