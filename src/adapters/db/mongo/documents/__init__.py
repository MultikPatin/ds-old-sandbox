import sys
from collections.abc import Sequence

from beanie import Document, UnionDoc, View

from .documents import (
    InputsDocument,
    InputSinglesDocument,
    InputTableDocument,
    InputTablesChunksDocument,
    KeysDocument,
    LayoutCardsDocument,
    LayoutHeaderCellsDocument,
    LayoutRequiredCellsDocument,
    LayoutRequiredRowsDocument,
    LayoutsDocument,
    LayoutSinglesDocument,
    LayoutStylesDocument,
    LayoutTablesDocument,
    LayoutTooltipsDocument,
    LayoutValidationsDocument,
    ModelsDocument,
    ParentLayout,
    ParentLayoutBlocks,
    ParentLayoutCells,
    ReferencesDocument,
)

__all__ = [
    "InputSinglesDocument",
    "InputTableDocument",
    "InputTablesChunksDocument",
    "InputsDocument",
    "KeysDocument",
    "LayoutCardsDocument",
    "LayoutHeaderCellsDocument",
    "LayoutRequiredCellsDocument",
    "LayoutRequiredRowsDocument",
    "LayoutSinglesDocument",
    "LayoutStylesDocument",
    "LayoutTablesDocument",
    "LayoutTooltipsDocument",
    "LayoutValidationsDocument",
    "LayoutsDocument",
    "ModelsDocument",
    "ParentLayout",
    "ParentLayoutBlocks",
    "ParentLayoutCells",
    "ReferencesDocument",
    "collect_documents",
]


async def collect_documents() -> Sequence[
    type[Document] | type[UnionDoc] | type[View]
]:
    from inspect import getmembers, isclass  # noqa: PLC0415

    return [
        doc
        for _, doc in getmembers(sys.modules[__name__], isclass)
        if issubclass(doc, Document | UnionDoc | View)
        and doc.__name__ not in ("Document", "UnionDoc", "View")
    ]
