# === ИМПОРТЫ ===
from bs4 import BeautifulSoup
import pandas as pd
import re

# === Загрузка HTML ===
with open(r'C:\Users\Mr.Chip\Desktop\DE sea\evangelion.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"✅ HTML загружен: {len(html)} символов\n")

soup = BeautifulSoup(html, "html.parser")

# === Парсинг товаров ===
products = soup.find_all('li', class_='product')

print(f"Найдено товаров: {len(products)}\n")

# Список для хранения данных
data = []

for i, product in enumerate(products, 1):
    # === 1. ID товара ===
    product_id = product.get('data-product-id')
    
    if not product_id:
        classes = product.get('class', [])
        for cls in classes:
            if cls.startswith('post-'):
                product_id = cls.replace('post-', '')
                break
    
    # === 2. Название товара ===
    title_el = product.find('span', class_='woocommerce-loop-product__title')
    name = title_el.text.strip() if title_el else None
    
    
    
    # === 3. Цена ===
    price_el = product.find('span', class_='price')
    price = price_el.text.strip() if price_el else None
    
    # === 4. Ссылка на товар ===
    link_el = product.find('a', class_='woocommerce-LoopProduct-link')
    product_url = link_el['href'] if link_el and link_el.has_attr('href') else None
    
    # === 5. Картинка товара ===
    img_el = product.find('img')
    img_url = None
    
    if img_el:
        
        # Из data-src
        if not img_url:
            img_url = img_el.get('data-src')
        
        # Делаем URL абсолютным
        if img_url and not img_url.startswith('http'):
            img_url = 'https://nikifilini.com' + img_url
    
    # === 6. Категории товара ===
    classes = product.get('class', [])
    categories = [c for c in classes if c.startswith('product_cat-')]
    category = ', '.join([c.replace('product_cat-', '') for c in categories]) if categories else None
    
    # === 7. Теги товара (цвета) ===
    tags = [c for c in classes if c.startswith('product_tag-')]
    tag = ', '.join([c.replace('product_tag-', '') for c in tags]) if tags else None
    
    # Добавляем данные в список
    data.append({
        'id': product_id,
        'name': name,
        'price': price,
        'product_url': product_url,
        'img_url': img_url,
        'category': category,
        'tags': tag
    })

# === Создание DataFrame ===
df = pd.DataFrame(data)

print(f"✅ Парсинг завершён!")
print(f"Собрано товаров: {len(df)}\n")

# === Вывод таблицы ===
print("Первые 5 товаров:\n")
print(df.head())

# === Сохранение в CSV ===
output_file = r'C:\Users\Mr.Chip\Desktop\DE sea\evangelion_products.csv'

try:
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ Данные сохранены в: {output_file}")
except PermissionError:
    output_file = r'C:\Users\Mr.Chip\Desktop\DE sea\evangelion_products_new.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ Данные сохранены в: {output_file}")

# === Статистика ===
print(f"\n📊 Статистика:")
print(f"Всего товаров: {len(df)}")
print(f"Товаров с ID: {df['id'].notna().sum()}")
print(f"Товаров с названием: {df['name'].notna().sum()}")
print(f"Товаров с ценой: {df['price'].notna().sum()}")
print(f"Товаров с картинкой: {df['img_url'].notna().sum()}")

# === Показать полную таблицу ===
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

print("\n📦 Полная таблица товаров:\n")
df