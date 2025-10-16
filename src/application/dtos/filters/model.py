from common.core.dtos import LifeStatusOrNoneDTO
from pydantic import Field


class ModelFilters(LifeStatusOrNoneDTO):
    sort: str | None = Field(default=None)
