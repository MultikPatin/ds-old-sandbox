import sys
from collections.abc import Sequence

from beanie import Document, UnionDoc, View

from .documents import (
    InputDocument,
    InputSingleDocument,
    InputTableChunkDocument,
    InputTableDocument,
    LayoutCardDocument,
    LayoutDefaultDocument,
    LayoutDocument,
    LayoutSchemaDocument,
    LayoutSingleDocument,
    LayoutStyleDocument,
    LayoutTableDocument,
    LayoutValidationDocument,
)

__all__ = [
    "InputDocument",
    "InputSingleDocument",
    "InputTableChunkDocument",
    "InputTableDocument",
    "LayoutCardDocument",
    "LayoutDefaultDocument",
    "LayoutDocument",
    "LayoutSchemaDocument",
    "LayoutSingleDocument",
    "LayoutStyleDocument",
    "LayoutTableDocument",
    "LayoutValidationDocument",
    "collect_documents",
]


def collect_documents() -> Sequence[
    type[Document] | type[UnionDoc] | type[View]
]:
    from inspect import getmembers, isclass  # noqa: PLC0415

    return [
        doc
        for _, doc in getmembers(sys.modules[__name__], isclass)
        if issubclass(doc, Document | UnionDoc | View)
        and doc.__name__ not in ("Document", "UnionDoc", "View")
    ]
