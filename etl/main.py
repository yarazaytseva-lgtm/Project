import argparse
from typing import Optional

try:
    from . import RAW_DIR, PROCESSED_DIR
    from .extract import extract
    from .load import load, save_processed
    from .transform import transform
    from .validate import validate_input, validate_output
except ImportError:  # running as a script instead of a module
    import pathlib
    import sys

    package_root = pathlib.Path(__file__).resolve().parent.parent
    if str(package_root) not in sys.path:
        sys.path.append(str(package_root))
    from etl import RAW_DIR, PROCESSED_DIR
    from etl.extract import extract
    from etl.load import load, save_processed
    from etl.transform import transform
    from etl.validate import validate_input, validate_output


def run_pipeline(file_id: str, table_name: str, limit: int, skip_db: bool) -> None:
    print(f"Извлечение из гугл диска '{file_id}'")
    raw_df = extract(file_id)
    validate_input(raw_df)

    print("Преобразование набора данных")
    transformed_df = transform(raw_df)
    validate_output(transformed_df)

    print(f"Сохранение обработанных данных в {PROCESSED_DIR}")
    if skip_db:
        save_processed(transformed_df)
    else:
        print("Загрузка данных в базу данных")
        load(transformed_df, table_name=table_name, limit=limit)

    print("ETL pipeline завершен")
    print(f"Исходный каталог: {RAW_DIR}")
    print(f"Обработанный каталог: {PROCESSED_DIR}")


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ETL pipeline runner")
    parser.add_argument("file_id", help="Google Drive file id for the source CSV")
    parser.add_argument(
        "--table-name",
        default="zaytseva",
        help="Destination table name in the target PostgreSQL database",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of rows to load into the database",
    )
    parser.add_argument(
        "--skip-db",
        action="store_true",
        help="Skip database load and only materialize processed files",
    )
    return parser.parse_args(args=args)


def main(argv: Optional[list[str]] = None) -> None:
    options = parse_args(argv)
    run_pipeline(
        file_id=options.file_id,
        table_name=options.table_name,
        limit=options.limit,
        skip_db=options.skip_db,
    )


if __name__ == "__main__":
    main()
