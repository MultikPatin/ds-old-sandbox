from pydantic import Field

from .db import (
    LayoutDB,
    LayoutDefaultDB,
    LayoutSchemaDB,
    LayoutSingleDB,
    LayoutStyleDB,
    LayoutTableDB,
    LayoutValidationDB,
)


class LayoutSingleWithLayersDTO(LayoutSingleDB):
    schemas: list[LayoutSchemaDB] | None = Field(default=None)  # type: ignore
    validations: list[LayoutValidationDB] | None = Field(default=None)  # type: ignore
    styles: list[LayoutStyleDB] | None = Field(default=None)  # type: ignore
    defaults: list[LayoutDefaultDB] | None = Field(default=None)  # type: ignore


class LayoutTableWithLayersDTO(LayoutTableDB):
    schemas: list[list[LayoutSchemaDB]] | None = Field(default=None)  # type: ignore
    validations: list[list[LayoutValidationDB]] | None = Field(default=None)  # type: ignore
    styles: list[list[LayoutStyleDB]] | None = Field(default=None)  # type: ignore
    defaults: list[list[LayoutDefaultDB]] | None = Field(default=None)  # type: ignore


class LayoutWithBlockLayersDTO(LayoutDB):
    singles: list[LayoutSingleWithLayersDTO] | None = Field(default=None)
    tables: list[LayoutTableWithLayersDTO] | None = Field(default=None)
