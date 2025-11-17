from common.mongo import AddMixin, GetByIDsMixin, GetMixin

from src.application.dtos.db import (
    LayoutSchemaCreateDTO,
    LayoutSchemaDB,
    LayoutStyleCreateDTO,
    LayoutStyleDB,
    LayoutValidationCreateDTO,
    LayoutValidationDB,
)


class LayoutCellRepository(
    GetMixin[LayoutSchemaDB],
    GetByIDsMixin[LayoutSchemaDB],
    AddMixin[LayoutSchemaCreateDTO, LayoutSchemaDB],
):
    pass


class LayoutStyleRepository(
    GetMixin[LayoutStyleDB],
    GetByIDsMixin[LayoutStyleDB],
    AddMixin[LayoutStyleCreateDTO, LayoutStyleDB],
):
    pass


class LayoutValidationRepository(
    GetMixin[LayoutValidationDB],
    GetByIDsMixin[LayoutValidationDB],
    AddMixin[LayoutValidationCreateDTO, LayoutValidationDB],
):
    pass
