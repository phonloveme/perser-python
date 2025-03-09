import requests
from bs4 import BeautifulSoup
import json

# Функция для получения HTML-кода страницы
def get_html_from_url(url):
    """
    Получает HTML-код страницы по указанному URL.
    
    :param url: URL страницы.
    :return: HTML-код страницы (строка).
             Если запрос не удался, возвращает None.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        response.encoding = 'utf-8'  # Установка кодировки
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


# Функция для парсинга новостей
def parse_news(html_document):
    """
    Парсит список новостей из HTML-документа.
    
    :param html_document: HTML-код страницы (строка).
    :return: Список словарей с данными новостей.
    """
    soup = BeautifulSoup(html_document, 'html.parser')
    news_list = []

    # Поиск блоков новостей
    news_blocks = soup.find_all('div', class_='list-entry')[:10]  # Берём первые 10 новостей

    for block in news_blocks:
        # Извлечение заголовка и ссылки
        title_tag = block.find('h5').find('a')
        title = title_tag.text.strip()
        href = title_tag['href'] if title_tag and 'href' in title_tag.attrs else "#"

        # Извлечение даты
        date_tag = block.find('p').find('small')
        date = date_tag.text.strip()

        # Извлечение intro текста
        intro_tag = block.find('div', style="text-align: justify;")
        intro = intro_tag.text.strip() if intro_tag else "Intro не указано"

        # Добавление новости в список
        news_list.append({
            "data": date,
            "href": href,
            "title": title,
            "text": intro
        })

    return news_list


# Функция для сохранения новостей в JSON-файл
def save_to_json(news_list, filename="news.json"):
    """
    Сохраняет список новостей в JSON-файл.
    
    :param news_list: Список словарей с данными новостей.
    :param filename: Имя файла для сохранения.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(news_list, file, ensure_ascii=False, indent=4)
    print(f"Новости успешно сохранены в файл: {filename}")


# Основная программа
if __name__ == "__main__":
    # URL страницы с новостями
    url = "https://pgsha.ru/today/"  # или "https://pgatu.ru/today/"

    # Получение HTML-кода страницы
    html_document = get_html_from_url(url)
    if html_document is None:
        print("Не удалось получить HTML-документ.")
    else:
        # Парсинг новостей
        news_list = parse_news(html_document)

        # Сохранение новостей в JSON-файл
        save_to_json(news_list)