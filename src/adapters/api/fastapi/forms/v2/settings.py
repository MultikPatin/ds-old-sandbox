from common.core.settings import set_model_config
from common.fastapi import VersionedAPISettings


class Settings(VersionedAPISettings):
    model_config = set_model_config(env_prefix="FORMS_API_V2_")
