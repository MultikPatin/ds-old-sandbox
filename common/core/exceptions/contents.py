from typing import Any

from pydantic import BaseModel, Field


class BaseErrorContent(BaseModel):
    message: str = Field(
        default="",
        description="Error message",
        max_length=1000,
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Error context",
    )


class BusinessLogicErrorContent(BaseErrorContent):
    pass


class LockedOperationErrorContent(BaseErrorContent):
    pass
