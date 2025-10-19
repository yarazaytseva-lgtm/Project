import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

# Чтение данных для подключения к PostgreSQL из переменных окружения
url = os.environ.get('POSTGRES_URL')
port = os.environ.get('POSTGRES_PORT')
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
dbname = os.environ.get('POSTGRES_DB')

# Проверка 
assert url, "Не задан POSTGRES_URL"
assert port, "Не задан POSTGRES_PORT"
assert user, "Не задан POSTGRES_USER"
assert password, "Не задан POSTGRES_PASSWORD"
assert dbname, "Не задан POSTGRES_DB"

# Подключение к PostgreSQL
print('\nПодключение к PostgreSQL')
conn_str = f'postgresql+psycopg2://{user}:{password}@{url}:{port}/{dbname}'
engine = create_engine(conn_str)
print('Подключение к PostgreSQL создано успешно')

# Загрузка датасета
print('\nЗагрузка датасета clean.parquet')
df = pd.read_parquet('data/clean.parquet')
print(f'Датасет успешно загружен. Всего строк: {len(df)}, столбцов: {len(df.columns)}')

# Первые 100 строк
df = df.head(100)
print(f'Подготовлено {len(df)} строк для записи в БД')

# Записываем данные в таблицу
table_name = 'zaytseva'
print(f'\nЗапись данных в таблицу "{table_name}" (схема public)')
df.to_sql(table_name, engine, schema="public", if_exists="replace", index=False)
print(f'Таблица "{table_name}" успешно записана ({len(df)} строк)')

# Проверяем запись
print('\nПроверка записи данных в таблицу')
with engine.connect() as conn:
    result = conn.execute(text(f'SELECT * FROM {table_name} LIMIT 3;'))
    rows = result.fetchall()

assert len(rows) > 0, "Ошибка: данные не записались в таблицу!"

print(f'Таблица "{table_name}" существует. Пример строк:')
for r in rows:
    print(r)

print('\nСкрипт завершен без ошибок')
