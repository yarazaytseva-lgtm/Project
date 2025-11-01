# Data-management-Engineering

Репозиторий для проекта "Инжиниринг управления данными ИТМО".

## Ссылки на датасеты

Ссылка на датасеты: [Папка на Google Drive](https://drive.google.com/drive/folders/1GvA6M1ma6kzHevxSzJbiYUt6M8fEsJ1H?usp=sharing) 

Исходный источник датасета: [CalCOFI на Kaggle](https://www.kaggle.com/datasets/sohier/calcofi?utm_source=chatgpt.com&select=cast.csv)

## Ссылка на EDA ноутбук

🔗 [Открыть EDA.ipynb в nbviewer](https://nbviewer.org/github/yarazaytseva-lgtm/Project/blob/main/notebooks/EDA.ipynb)
 > Визуализация в самом конце 

## ETL пакет

```
etl/
	extract.py     # скачивание исходного CSV и сохранение в data/raw
	transform.py   # приведение типов и прочие преобразования
	validate.py    # проверки входных и выходных данных
	load.py        # сохранение обработанных данных и выгрузка в БД
	main.py        # CLI-обёртка, связывающая все шаги
data/
	raw/           # сохраняются сырые выгрузки
	processed/     # итоговые clean.csv и clean.parquet
---

> **Примечание:** Папка `archive/` содержит старые версии и дополнительные учебные материалы.


## Инструкция по запуску

### 1. Создать виртуальное окружение
```
python -m venv .venv
```

### 2. Активировать виртуальное окружение
```
.\.venv\Scripts\activate
```

### 3. Установить зависимости
```
pip install -r requirements.txt
```

### 4. Подготовить переменные окружения
Создайте файл `.env` в корне или задайте переменные оболочки с параметрами подключения к PostgreSQL:
```
POSTGRES_URL=<host>
POSTGRES_PORT=<port>
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database>
```

### 5. Запустить ETL-pipeline
```
python -m etl.main <GOOGLE_DRIVE_FILE_ID> [--table-name my_table] [--limit 100] [--skip-db]
```
- обязательный позиционный аргумент `GOOGLE_DRIVE_FILE_ID` — идентификатор CSV в Google Drive;
- `--table-name` — имя таблицы в PostgreSQL (по умолчанию `zaytseva`);
- `--limit` — максимум строк, которые будут выгружены в БД (по умолчанию `100`);
- `--skip-db` — пропустить этап записи в БД и сохранить только файлы в `data/processed`.

Самый простой пример запуска без загрузки в БД:
```
python -m etl.main 10eufblSIFd0USk8-6YX2O5NyMI1RlaP- --skip-db
```

## Пример вывода скрипта

**Вывод**:<img width="1113" height="511" alt="image" src="https://github.com/user-attachments/assets/54853796-a311-4344-a7dc-8fe9b9458fee" />
