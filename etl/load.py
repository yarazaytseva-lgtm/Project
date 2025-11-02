import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from . import PROCESSED_DIR

DEFAULT_TABLE_NAME = "zaytseva"
DEFAULT_PARQUET_NAME = "clean.parquet"


def save_processed(df: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    parquet_path = PROCESSED_DIR / DEFAULT_PARQUET_NAME
    df.to_parquet(parquet_path, index=False)
   

def _build_connection_string() -> str:
    load_dotenv()
    url = os.environ.get("POSTGRES_URL")
    port = os.environ.get("POSTGRES_PORT")
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")
    dbname = os.environ.get("POSTGRES_DB")

    missing = [name for name, value in {
        "POSTGRES_URL": url,
        "POSTGRES_PORT": port,
        "POSTGRES_USER": user,
        "POSTGRES_PASSWORD": password,
        "POSTGRES_DB": dbname,
    }.items() if not value]

    if missing:
        raise EnvironmentError(f"Missing required database settings: {', '.join(missing)}")

    return f"postgresql+psycopg2://{user}:{password}@{url}:{port}/{dbname}"


def load_to_database(df: pd.DataFrame, table_name: str = DEFAULT_TABLE_NAME, limit: int = 100) -> None:
    limited_df = df.head(limit).copy()
    if limited_df.empty:
        raise ValueError("No data available to load into the database")

    conn_str = _build_connection_string()
    engine = create_engine(conn_str)

    limited_df.to_sql(table_name, engine, schema="public", if_exists="replace", index=False)

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
        row_count = result.scalar() or 0
    if row_count != len(limited_df):
        raise RuntimeError(
            f"Row count mismatch after load: expected {len(limited_df)}, got {row_count}"
        )


def load(df: pd.DataFrame, table_name: str = DEFAULT_TABLE_NAME, limit: int = 100) -> None:
    # keep orchestration clear for main pipeline
    save_processed(df)
    load_to_database(df, table_name=table_name, limit=limit)

