MAX_ROW_COUNT_PER_CHUNK = 50
MAX_NUMBER_OF_CHUNKS = 1000

STORAGE_API_ENV_PREFIX = "STORAGE_"
CONSTRUCTOR_API_ENV_PREFIX = "CONSTRUCTOR_"


def get_versioned_prefix(prefix: str, version: int) -> str:
    if not prefix.endswith("_"):
        prefix = prefix + "_"
    return f"{prefix}API_V{version}_"
