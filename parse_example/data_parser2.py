import requests
from bs4 import BeautifulSoup
import pandas as pd


url = 'https://quotes.toscrape.com/'
response = requests.get(url)

# Проверяем, что запрос прошёл успешно
if response.status_code == 200:
    html = response.text
    print(f"✅ HTML скачан: {len(html)} символов\n")
else:
    print(f"❌ Ошибка: {response.status_code}")
    exit()


soup = BeautifulSoup(html, 'html.parser')

# Ищем все цитаты - элементы с классом 'quote'
quotes = soup.find_all('div', class_='quote')
print(f"Найдено цитат: {len(quotes)}\n")


data = []

for i, quote in enumerate(quotes, 1):
    # Текст цитаты 
    text_el = quote.find('span', class_='text')
    text = text_el.text.strip() if text_el else None
    
    # Автор 
    author_el = quote.find('small', class_='author')
    author = author_el.text.strip() if author_el else None
    
    # Теги 
    tags_el = quote.find_all('a', class_='tag')
    tags = ', '.join([tag.text.strip() for tag in tags_el]) if tags_el else None
    
    # Добавляем данные в список
    data.append({
        'номер': i,
        'цитата': text,
        'автор': author,
        'теги': tags
    })
    
    print(f"{i}. {author}: {text[:50]}...")  # Выводим первые 50 символов


df = pd.DataFrame(data)

print(f"\n✅ Парсинг завершён!")
print(f"Собрано цитат: {len(df)}\n")


print("Первые 5 цитат:\n")
print(df.head())

output_file = 'quotes.csv'

df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n✅ Данные сохранены в: {output_file}")

# === СТАТИСТИКА ===
print(f"\n📊 Статистика:")
print(f"Всего цитат: {len(df)}")
print(f"Уникальных авторов: {df['автор'].nunique()}")
print(f"Цитат с тегами: {df['теги'].notna().sum()}")
