from pydantic import BaseModel, Field

from .db import (
    LayoutDB,
    LayoutDefaultDB,
    LayoutMessageDB,
    LayoutSchemaDB,
    LayoutSingleDB,
    LayoutStyleDB,
    LayoutTableDB,
    LayoutValidationDB,
)

type Schemas = list[LayoutSchemaDB] | None
type Defaults = list[LayoutDefaultDB | None] | None
type Validations = list[LayoutValidationDB | None] | None
type Styles = list[LayoutStyleDB | None] | None


class LayoutSingleWithLayersDTO(LayoutSingleDB):
    schemas: Schemas = Field(default=None)  # type: ignore
    defaults: Defaults = Field(default=None)  # type: ignore
    validations: Validations = Field(default=None)  # type: ignore
    styles: Styles = Field(default=None)  # type: ignore


class LayoutTableWithLayersDTO(LayoutTableDB):
    schemas: list[Schemas] | None = Field(default=None)  # type: ignore
    defaults: list[Defaults] | None = Field(default=None)  # type: ignore
    validations: Validations = Field(default=None)  # type: ignore
    styles: Styles = Field(default=None)  # type: ignore


class LayoutWithBlockLayersDTO(LayoutDB):
    singles: list[LayoutSingleWithLayersDTO] | None = Field(default=None)
    tables: list[LayoutTableWithLayersDTO] | None = Field(default=None)
    messages: list[LayoutMessageDB] | None = Field(default=None)


class LayoutMessageCreate(BaseModel):
    is_hidden: bool = Field(default=True)
    text: str = Field(min_length=1, max_length=512)
    color: str = Field(default="#FFFFFF", min_length=7, max_length=7)
