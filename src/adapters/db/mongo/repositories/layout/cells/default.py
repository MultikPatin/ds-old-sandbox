from src.application.dtos.db import (
    LayoutDefaultCreateDTO,
    LayoutDefaultDB,
    LayoutDefaultUpdateDTO,
)

from .base import _Repository


class LayoutDefaultRepository(
    _Repository[
        LayoutDefaultDB,
        LayoutDefaultCreateDTO,
        LayoutDefaultUpdateDTO,
    ]
):
    pass
