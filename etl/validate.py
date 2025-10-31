from collections.abc import Iterable

import pandas as pd

_REQUIRED_COLUMNS = {
    "Cruise_ID",
    "Cast_ID",
    "Date",
    "Time",
    "Lat_Dec",
    "Lon_Dec",
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

