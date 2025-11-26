from src.application.dtos.db import (
    LayoutSchemaCreateDTO,
    LayoutSchemaDB,
    LayoutSchemaUpdateDTO,
)

from .base import _Repository


class LayoutSchemaRepository(
    _Repository[
        LayoutSchemaDB,
        LayoutSchemaCreateDTO,
        LayoutSchemaUpdateDTO,
    ]
):
    pass
