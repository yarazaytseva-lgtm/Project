import pandas as pd


DATE_COLUMNS = [
    "Date",
    "Time",
    "Inc_Str",
    "Inc_End",
    "PST_LAN",
    "Civil_T",
    "RecipeDate",
    "Receipt Date",
    "Pickup Time",
]
FLOAT_COLUMNS: list[str] = []
INT_COLUMNS: list[str] = []
BOOL_COLUMNS: list[str] = []
CAT_COLUMNS: list[str] = []


def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.convert_dtypes()

    for column in FLOAT_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("float64")
    for column in INT_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
    for column in BOOL_COLUMNS:
        if column in df.columns:
            df[column] = df[column].map({"1": True, "0": False, 1: True, 0: False}).astype("boolean")
    for column in DATE_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce", dayfirst=True)
    for column in CAT_COLUMNS:
        if column in df.columns:
            df[column] = df[column].astype("category")

    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    # separate function keeps orchestration code clean
    return enforce_schema(df)
