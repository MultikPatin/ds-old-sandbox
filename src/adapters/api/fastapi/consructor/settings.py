from common.core.settings import set_model_config
from common.fastapi import MainAPISettings


class Settings(MainAPISettings):
    model_config = set_model_config(env_prefix="CONSTRUCTOR_")
