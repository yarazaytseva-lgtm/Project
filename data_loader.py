import pathlib
import pandas as pd
from data_convert import enforce_schema

DATA_DIR = pathlib.Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

FILE_ID = "10eufblSIFd0USk8-6YX2O5NyMI1RlaP-"
FILE_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

def load_raw() -> pd.DataFrame:
    df = pd.read_csv(FILE_URL, encoding="utf-8", sep=",", na_values=["", "NA", "NaN", "null"], low_memory=False)
    return df


def save(df: pd.DataFrame):
    (DATA_DIR / "clean.csv").write_text("", encoding="utf-8")  # гарантируем путь
    df.to_csv(DATA_DIR / "clean.csv", index=False, encoding="utf-8")
    try:
        df.to_parquet(DATA_DIR / "clean.parquet", index=False)
    except Exception as e:
        print("Parquet не сохранился:", e)

def main():
    
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        df = load_raw()
        print("До:\n", df.dtypes)
        df=enforce_schema(df)
        
        print("После:\n", df.dtypes)
        save(df)


if name == "main":
    main()


