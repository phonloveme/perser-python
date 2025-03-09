import re
import requests

def find_next_hyperlink(document, start_pos):
    """
    Ищет ближайший тег гиперссылки <a> в документе с текущей позиции.
    
    :param document: Исходный HTML-документ (строка).
    :param start_pos: Позиция, с которой начинается поиск.
    :return: Кортеж (позиция после окончания тега, гиперссылка, текст названия).
             Если тег не найден, возвращает None.
    """
    # Регулярное выражение для поиска тега <a>
    pattern = re.compile(
        r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>', 
        re.IGNORECASE | re.DOTALL
    )
    
    # Поиск первого совпадения с текущей позиции
    match = pattern.search(document, pos=start_pos)
    
    if match:
        # Извлечение данных из совпадения
        href = match.group(1)  # Гиперссылка (значение href)
        name = match.group(2).strip()  # Текст ссылки (между <a> и </a>)
        end_pos = match.end()  # Позиция после окончания тега
        
        return end_pos, href, name
    
    # Если тег не найден
    return None


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


def find_all_hyperlinks(html_document):
    """
    Находит все гиперссылки в HTML-документе.
    
    :param html_document: HTML-код страницы (строка).
    :return: Список кортежей (гиперссылка, текст названия).
    """
    hyperlinks = []
    current_pos = 0
    
    while True:
        result = find_next_hyperlink(html_document, current_pos)
        if result is None:
            break
        
        # Распаковка результата
        end_pos, href, name = result
        hyperlinks.append((href, name))
        current_pos = end_pos  # Обновление позиции для следующего поиска
    
    return hyperlinks


# Основная программа
if __name__ == "__main__":
    # URL страницы
    url = "https://pcoding.ru/darkNet.php"
    
    # Получение HTML-кода страницы
    html_document = get_html_from_url(url)
    if html_document is None:
        print("Не удалось получить HTML-документ.")
    else:
        # Поиск всех гиперссылок
        hyperlinks = find_all_hyperlinks(html_document)
        
        # Вывод результатов
        print("Найденные гиперссылки:")
        for idx, (href, name) in enumerate(hyperlinks, 1):
            print(f"{idx}. href: {href}, name: {name}")