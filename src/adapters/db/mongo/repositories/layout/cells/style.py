from src.application.dtos.db import (
    LayoutStyleCreateDTO,
    LayoutStyleDB,
    LayoutStyleUpdateDTO,
)

from .base import _Repository


class LayoutStyleRepository(
    _Repository[
        LayoutStyleDB,
        LayoutStyleCreateDTO,
        LayoutStyleUpdateDTO,
    ]
):
    pass
