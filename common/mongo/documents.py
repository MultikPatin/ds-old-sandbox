from typing import TypeVar

from beanie import Document

DocType = TypeVar("DocType", bound=Document)
