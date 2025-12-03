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

type Schemas = list[LayoutSchemaDB]
type Defaults = list[LayoutDefaultDB | None] | None
type Validations = list[LayoutValidationDB | None] | None
type Styles = list[LayoutStyleDB | None] | None


class LayoutSingleWithLayersDTO(LayoutSingleDB):
    schemas: Schemas  # type: ignore
    defaults: Defaults = Field(default=None)  # type: ignore
    validations: Validations = Field(default=None)  # type: ignore
    styles: Styles = Field(default=None)  # type: ignore


class LayoutTableWithLayersDTO(LayoutTableDB):
    schemas: list[Schemas]  # type: ignore
    defaults: list[Defaults] | None = Field(default=None)  # type: ignore
    validations: Validations = Field(default=None)  # type: ignore
    styles: Styles = Field(default=None)  # type: ignore


class LayoutWithBlockLayersDTO(LayoutDB):
    singles: list[LayoutSingleWithLayersDTO] | None = Field(default=None)
    tables: list[LayoutTableWithLayersDTO] | None = Field(default=None)
