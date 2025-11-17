from pydantic import Field

from .db import (
    LayoutDB,
    LayoutSchemaDB,
    LayoutSingleDB,
    LayoutStyleDB,
    LayoutTableDB,
    LayoutValidationDB,
)


class LayoutSingleWithLayersDTO(LayoutSingleDB):
    schemas: list[LayoutSchemaDB] | None = Field(default=None)
    validations: list[LayoutValidationDB] | None = Field(default=None)
    styles: list[LayoutStyleDB] | None = Field(default=None)


class LayoutTableWithLayersDTO(LayoutTableDB):
    schemas: list[list[LayoutSchemaDB]] | None = Field(default=None)
    validations: list[list[LayoutValidationDB]] | None = Field(default=None)
    styles: list[list[LayoutStyleDB]] | None = Field(default=None)


class LayoutWithBlockLayersDTO(LayoutDB):
    singles: list[LayoutSingleWithLayersDTO] | None = Field(default=None)
    tables: list[LayoutTableWithLayersDTO] | None = Field(default=None)
