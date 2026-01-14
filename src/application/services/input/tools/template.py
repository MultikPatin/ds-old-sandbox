from typing import TYPE_CHECKING

from src.application.dtos import (
    InputCreateValuesDTO,
    InputSingleCreateValuesDTO,
    InputTableCreateValuesDTO,
)

if TYPE_CHECKING:
    from src.application.dtos import (
        LayoutSingleWithLayersDTO,
        LayoutTableWithLayersDTO,
        LayoutWithBlockLayersDTO,
    )
    from src.application.dtos.db import LayoutDefaultDB

type DefaultsItems = list[LayoutDefaultDB | None]
type DefaultsRows = list[str | None]


def generate_template(
    layout: "LayoutWithBlockLayersDTO",
) -> InputCreateValuesDTO:
    singles = [_singles(s) for s in layout.singles] if layout.singles else None
    tables = [_tables(t) for t in layout.tables] if layout.tables else None
    return InputCreateValuesDTO(
        layout=layout.id,
        singles=singles,
        tables=tables,
    )


def _singles(item: "LayoutSingleWithLayersDTO") -> InputSingleCreateValuesDTO:
    if item.schemas is None:
        msg = "For generate template, schemas must be set in layout."
        raise ValueError(msg)

    keys = [s.key for s in item.schemas]

    # TODO Проработать вариант типизации defaults

    values = set_defaults_row(item.defaults, len(keys))

    return InputSingleCreateValuesDTO(
        key=item.key,
        values=dict(zip(keys, values, strict=False)),
    )


def _tables(
    item: "LayoutTableWithLayersDTO",
) -> InputTableCreateValuesDTO:
    if item.schemas is None:
        msg = "For generate template, schemas must be set in layout."
        raise ValueError(msg)

    columns = len(item.schemas[-1])

    # TODO Проработать вариант типизации defaults

    if item.defaults is None:
        row = [None for _ in range(columns)]
        return InputTableCreateValuesDTO(key=item.key, values=[row])

    rows = [set_defaults_row(d, columns) for d in item.defaults]

    return InputTableCreateValuesDTO(key=item.key, values=rows)


def set_defaults_row(
    items: DefaultsItems | None, row_length: int
) -> DefaultsRows:
    if items is None:
        return [None for _ in range(row_length)]

    values = [item if item is None else item.value for item in items]
    vl = len(values)

    if vl > row_length:
        msg = "incorrect number of defaults"
        raise ValueError(msg)
    if vl < row_length:
        values.extend([None for _ in range(row_length - vl)])

    return values
