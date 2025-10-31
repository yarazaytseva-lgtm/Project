from pathlib import Path
from typing import Optional

import pandas as pd
import requests

from . import RAW_DIR

NA_VALUES = ["", "NA", "NaN", "null"]
CSV_ENCODING = "utf-8"
CSV_SEPARATOR = ","
DEFAULT_RAW_NAME = "raw.csv"


def build_drive_url(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def download_raw_csv(file_id: str, destination: Optional[Path] = None) -> Path:
    destination = destination or RAW_DIR / DEFAULT_RAW_NAME
    destination.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(build_drive_url(file_id), timeout=120)
    response.raise_for_status()
    destination.write_bytes(response.content)
    return destination


def load_raw_dataframe(source: Path) -> pd.DataFrame:
    return pd.read_csv(
        source,
        encoding=CSV_ENCODING,
        sep=CSV_SEPARATOR,
        na_values=NA_VALUES,
        low_memory=False,
    )


def extract(file_id: str) -> pd.DataFrame:
    raw_path = download_raw_csv(file_id)
    return load_raw_dataframe(raw_path)

