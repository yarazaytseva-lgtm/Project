#  Парсер цитат с Quotes.toscrape.com

Cобирает цитаты известных людей с сайта [Quotes to Scrape](https://quotes.toscrape.com/) и сохраняет их в CSV-файл.

## Описание

Программа скачивает HTML-страницу, парсит её и извлекает:
- Текст цитаты
- Автора цитаты
- Теги (категории)

Все данные сохраняются в CSV-файл для дальнейшего анализа.

## Проект использует следующие библиотеки Python:

- **requests** - для скачивания HTML-страниц
- **BeautifulSoup4** - для парсинга HTML
- **pandas** - для работы с данными и экспорта в CSV

## Требования

Для запуска проекта необходим Python 3.7 или выше и следующие библиотеки:

pip install requests beautifulsoup4 pandas

## Пример вывода
<img width="1136" height="213" alt="image" src="https://github.com/user-attachments/assets/3bdc41e6-0efd-494d-a18e-37920e78f1ea" />
