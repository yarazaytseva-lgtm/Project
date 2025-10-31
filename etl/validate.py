from collections.abc import Iterable

import pandas as pd

_REQUIRED_COLUMNS = {
    "Patient name",
    "Company Name",
    "Drug Name",
    "Receipt Date",
}


def _missing_columns(df: pd.DataFrame, required: Iterable[str]) -> set[str]:
    return set(required) - set(df.columns)


def validate_input(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Input dataset is empty")
    missing = _missing_columns(df, _REQUIRED_COLUMNS)
    if missing:
        raise ValueError(f"Input dataset is missing required columns: {sorted(missing)}")


def validate_output(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Transformed dataset is empty")
    missing = _missing_columns(df, _REQUIRED_COLUMNS)
    if missing:
        raise ValueError(f"Transformed dataset lost required columns: {sorted(missing)}")
