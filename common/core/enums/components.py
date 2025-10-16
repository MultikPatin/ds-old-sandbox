from enum import StrEnum, auto


class ComponentsEnum(StrEnum):
    redis = auto()
    mongo = auto()
    elasticsearch = auto()
    postgres = auto()
    clickhouse = auto()
    minio = auto()
    faststream = auto()
    rabbitmq = auto()
    kafka = auto()
    fastapi = auto()
    litestar = auto()
    falcon = auto()
