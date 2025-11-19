import hashlib
import json

from common.core.custom_types import AnyDict, AnyList

__all__ = ["get_md5hash", "get_sha256hash"]


def get_md5hash(instance: AnyDict | AnyList, hex_digest: int = 24) -> str:
    return hashlib.md5(  # noqa: S324
        json.dumps(
            instance,
            sort_keys=True,
            ensure_ascii=True,
        ).encode("utf-8")
    ).hexdigest()[:hex_digest]


def get_sha256hash(instance: AnyDict | AnyList, hex_digest: int = 24) -> str:
    return hashlib.sha256(
        json.dumps(
            instance,
            sort_keys=True,
            ensure_ascii=True,
        ).encode("utf-8")
    ).hexdigest()[:hex_digest]
