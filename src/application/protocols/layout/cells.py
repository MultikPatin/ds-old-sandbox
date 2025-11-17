from typing import Protocol

from common.core.protocols import (
    AdderProtocol,
    GetterByIDsProtocol,
    GetterProtocol,
    SessionProtocol,
)

from src.application.dtos.db import (
    LayoutSchemaCreateDTO,
    LayoutSchemaDB,
    LayoutStyleCreateDTO,
    LayoutStyleDB,
    LayoutValidationCreateDTO,
    LayoutValidationDB,
)


class LayoutSchemaServiceProtocol(
    GetterByIDsProtocol[LayoutSchemaDB, SessionProtocol],
    Protocol,
): ...


class LayoutStyleServiceProtocol(
    GetterByIDsProtocol[LayoutStyleDB, SessionProtocol],
    Protocol,
): ...


class LayoutValidationServiceProtocol(
    GetterByIDsProtocol[LayoutValidationDB, SessionProtocol],
    Protocol,
): ...


class LayoutSchemaRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutSchemaDB, Session],
    GetterByIDsProtocol[LayoutSchemaDB, Session],
    AdderProtocol[LayoutSchemaCreateDTO, LayoutSchemaDB, Session],
    Protocol,
): ...


class LayoutStyleRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutStyleDB, Session],
    GetterByIDsProtocol[LayoutStyleDB, Session],
    AdderProtocol[LayoutStyleCreateDTO, LayoutStyleDB, Session],
    Protocol,
): ...


class LayoutValidationRepositoryProtocol[Session: SessionProtocol](
    GetterProtocol[LayoutValidationDB, Session],
    GetterByIDsProtocol[LayoutValidationDB, Session],
    AdderProtocol[LayoutValidationCreateDTO, LayoutValidationDB, Session],
    Protocol,
): ...
