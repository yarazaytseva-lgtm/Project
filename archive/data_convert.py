import pandas as pd

def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:

    df = df.convert_dtypes()

    # замените списки колонок на свои реальные имена
    int_cols    = []
    float_cols  = []
    bool_cols   = []
    date_cols   = ["Date", "Time", "Inc_Str", "Inc_End", "PST_LAN", "Civil_T"]
    cat_cols    = []

    # числа
    for c in float_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("float64")
    for c in int_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    # булевы
    for c in bool_cols:
        if c in df.columns:
            df[c] = df[c].map({"1": True, "0": False, 1: True, 0: False}).astype("boolean")
    # даты
    for c in date_cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", dayfirst=True)
    # категории
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype("category")
    return df
