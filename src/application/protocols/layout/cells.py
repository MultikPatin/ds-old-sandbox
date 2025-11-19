from typing import TYPE_CHECKING, Protocol

from common.core.protocols import (
    AdderProtocol,
    DecRefCountProtocol,
    DeleterProtocol,
    DeleteWithRefCountProtocol,
    GetterByHashProtocol,
    GetterByIDsProtocol,
    GetterProtocol,
    IncRefCountProtocol,
    SessionProtocol,
    UpdaterProtocol,
)

from src.application.dtos.db import (
    LayoutSchemaCreateDTO,
    LayoutSchemaDB,
    LayoutSchemaUpdateDTO,
    LayoutStyleCreateDTO,
    LayoutStyleDB,
    LayoutStyleUpdateDTO,
    LayoutValidationCreateDTO,
    LayoutValidationDB,
    LayoutValidationUpdateDTO,
)

if TYPE_CHECKING:
    from pydantic import BaseModel


class _ServiceProtocol[
    ReturnSchema: BaseModel,
    CreateSchema: BaseModel,
    UpdateSchema: BaseModel,
](
    GetterProtocol[ReturnSchema, SessionProtocol],
    GetterByIDsProtocol[ReturnSchema, SessionProtocol],
    AdderProtocol[CreateSchema, ReturnSchema, SessionProtocol],
    UpdaterProtocol[UpdateSchema, ReturnSchema, SessionProtocol],
    DeleterProtocol[SessionProtocol],
    Protocol,
): ...


class _RepositoryProtocol[
    ReturnSchema: BaseModel,
    CreateSchema: BaseModel,
    UpdateSchema: BaseModel,
    Session: SessionProtocol,
](
    GetterProtocol[ReturnSchema, Session],
    GetterByIDsProtocol[ReturnSchema, Session],
    GetterByHashProtocol[ReturnSchema, Session],
    AdderProtocol[CreateSchema, ReturnSchema, Session],
    UpdaterProtocol[UpdateSchema, ReturnSchema, Session],
    DecRefCountProtocol[Session],
    IncRefCountProtocol[Session],
    DeleteWithRefCountProtocol[Session],
    Protocol,
): ...


class LayoutSchemaServiceProtocol(
    _ServiceProtocol[
        LayoutSchemaDB,
        LayoutSchemaCreateDTO,
        LayoutSchemaUpdateDTO,
    ],
    Protocol,
): ...


class LayoutStyleServiceProtocol(
    _ServiceProtocol[
        LayoutStyleDB,
        LayoutStyleCreateDTO,
        LayoutStyleUpdateDTO,
    ],
    Protocol,
): ...


class LayoutValidationServiceProtocol(
    _ServiceProtocol[
        LayoutValidationDB,
        LayoutValidationCreateDTO,
        LayoutValidationUpdateDTO,
    ],
    Protocol,
): ...


class LayoutSchemaRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutSchemaDB,
        LayoutSchemaCreateDTO,
        LayoutSchemaUpdateDTO,
        Session,
    ],
    Protocol,
): ...


class LayoutStyleRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutStyleDB,
        LayoutStyleCreateDTO,
        LayoutStyleUpdateDTO,
        Session,
    ],
    Protocol,
): ...


class LayoutValidationRepositoryProtocol[Session: SessionProtocol](
    _RepositoryProtocol[
        LayoutValidationDB,
        LayoutValidationCreateDTO,
        LayoutValidationUpdateDTO,
        Session,
    ],
    Protocol,
): ...
