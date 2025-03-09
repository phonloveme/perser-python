import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

# URL страницы для парсинга
url = 'https://pcoding.ru/darkNet.php'

# Получение содержимого страницы
response = requests.get(url)
response.encoding = 'utf-8'

# Парсинг HTML с помощью BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Сбор всех ссылок на PDF
pdf_links = []
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if href.lower().endswith('.pdf'):
        # Преобразование относительной ссылки в абсолютную
        absolute_url = urljoin(url, href)
        # Получение названия документа (текст ссылки)
        name = a_tag.text.strip()
        pdf_links.append((absolute_url, name))

# Подготовка данных для CSV
rows = []
for idx, (href, name) in enumerate(pdf_links, 1):
    rows.append([idx, href, name])

# Запись в CSV-файл
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['id', 'href', 'name'])
    writer.writerows(rows)