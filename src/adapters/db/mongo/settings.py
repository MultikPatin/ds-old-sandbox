from common.core.settings import set_model_config
from common.mongo import Settings


class _Settings(Settings):
    model_config = set_model_config(env_prefix="MONGODB_")
