from src.application.dtos.db import (
    LayoutValidationCreateDTO,
    LayoutValidationDB,
    LayoutValidationUpdateDTO,
)

from .base import _Repository


class LayoutValidationRepository(
    _Repository[
        LayoutValidationDB,
        LayoutValidationCreateDTO,
        LayoutValidationUpdateDTO,
    ]
):
    pass
