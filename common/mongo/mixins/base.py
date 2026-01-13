from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from beanie import Document
    from pydantic import BaseModel


class Base:
    def __init__[DocType: Document](self, collection: type[DocType]) -> None:
        self._collection = collection


class BaseDTO[ReturnSchema: BaseModel](Base):
    def __init__[DocType: Document](
        self, collection: type[DocType], dto: type[ReturnSchema]
    ) -> None:
        super().__init__(collection)
        self._dto = dto
