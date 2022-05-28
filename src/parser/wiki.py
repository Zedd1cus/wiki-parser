"""
Этот код анализирует случайную статью в Википедии:
1. Подсчитывает, сколько раз каждое слово встречается в статье.
2. В тексте находит ссылки на другие статьи википедии и выполняет (1.) с каждой из них.
"""
import re
import os
import time
import shutil
from urllib.request import urlopen
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import List, Union
from bs4 import BeautifulSoup
from src.parser.file import list_writer, files_merge
from src.maps.hash_map import HashMap

ARTICLES_DIRECTORY = os.path.abspath('../../../../wiki/articles')  # место, где записываются данные статей
WIKI_RANDOM = "https://ru.wikipedia.org/wiki/Special:Random"
WIKI_DOMAIN = "https://ru.wikipedia.org"


def count_words(html_txt: str, hash_map: HashMap) -> HashMap:
    """
    Подсчитывает слова в статье Википедии.
    Хэш-таблица используется для подсчета слов. Ключ - это слово, а значение - номер слова в статье.
    :param html_txt: html-текст вики-статьи
    :param hash_map: хэш-таблица для записи результатов
    :return: хэш-таблица (ключ, значение = слово, количество слов)
    """
    soup = BeautifulSoup(html_txt, 'html.parser')
    main_txt = soup.find(id="mw-content-text").div
    splitters = (r'\s', r'\.', r'\!', r'\?', r',', r';',
                 r'править \| править код',
                 r'\[', r'\]', r'\(', r'\)', r'\n', r'\\', r'\|')
    splitters = r'|'.join(splitters)  # при этом строки слов будут разделены
    words = re.split(splitters, main_txt.get_text())
    for word in words:
        if word != '' and word.isalpha():  # чтобы подсчитать числа, isalpha следует изменить на isalnum
            lower_word = word.lower()
            hash_map[lower_word] = hash_map.get(lower_word, 0) + 1
    return hash_map


def get_urls(html_txt: str, max_urls=-1) -> list:
    """
    В данной статье википедии находятся ссылки на другие статьи википедии
    :param html_txt: html-текст вики-статьи
    :param max_urls: количество требуемых URL-адресов (default "-1" означает "all")
    :return: набор URL-адресов (list)
    """
    url_set = set()
    urls = 0
    soup = BeautifulSoup(html_txt, 'html.parser')
    main_txt = soup.find(id="mw-content-text").div
    for link in main_txt.find_all('a'):
        article_link = link.get('href')
        if article_link is not None and url_is_valid(article_link):
            if WIKI_DOMAIN + article_link not in url_set:  # добавляет только уникальные URL-адреса
                urls += 1
            url_set.add(WIKI_DOMAIN + article_link)
            if urls >= max_urls >= 0:
                return list(url_set)
    return list(url_set)


def url_is_valid(url: str) -> bool:
    """
    Проверяет, ведет ли URL-адрес на другую статью в Википедии
    :param url: URL-адрес
    :return: true if url is valid / false if not
    """
    black_list = ['gif', 'jpg', 'svg', 'png', 'ogg']
    if not url.startswith('/wiki/'):
        return False
    if url[-3:len(url)].lower() in black_list:
        return False
    if ':' in url or 'Edit' in url or url.endswith('#identifiers'):
        return False
    return True


def multi_parsing(url: str, mode: Union[ThreadPoolExecutor, Pool], depth: int = 0) -> None:
    """
    Анализирует статьи из базовых статей (найденные ссылки) и может повторяться несколько раз
    :param url: ссылка на базовую статью
    :param mode: multi[threading|processing]
    :param depth: depth of parsing
    :return: None
    """
    curr_urls = [[url]]
    for _ in range(depth+1):
        curr_urls = [new_url for urls in curr_urls for new_url in urls]
        with mode(32) as executor:
            curr_urls = executor.map(wiki_parser, curr_urls)


def wiki_parser(url: str, base_path=ARTICLES_DIRECTORY) -> List[str]:
    """
    1) Получает заголовок статьи из URL-адреса
    2) Если папка с таким заголовком, URL, содержимым, файлами word существует,
    то считывает содержимое и возвращает URL-адреса из содержимого, остальное идет дальше
    3) Отправляет запрос, получает содержимое страницы и URL-адрес
    4) Если папка не существует, функция создает каталог (заголовок его имени) и записывает в url
    5) Если файл содержимого не существует, он будет записан в двоичный файл
    6) Если файл words не существует, слова будут подсчитаны (в алфавитном порядке) и записаны
    7) Получает URL-адреса из содержимого (сначала оно декодируется) и возвращает их

    :param url: ссылка на статью
    :param base_path: путь, куда записывать файлы с содержимым и т.д.
    :return: список с найденными URL-адресами wiki (list)
    """
    heading = unquote(url).split('/wiki/')[-1].replace('_', ' ')

    # проверяет, ведет ли URL-адрес к случайной статье
    is_random = False
    if heading == 'Special:Random':
        is_random = True
        with urlopen(url) as response:
            curr_url = response.geturl()
            heading = unquote(curr_url).replace('_', ' ').split('/wiki/')[-1]
            content = response.read()

    heading = heading.replace('?', '(q.mark)')

    # проверяет, существует ли уже папка статьи
    folder_exists = heading in os.listdir(base_path)
    current_path = os.path.join(base_path, heading)

    url_path = os.path.join(current_path, 'url.txt')
    content_path = os.path.join(current_path, 'content.txt')
    words_path = os.path.join(current_path, 'words.txt')

    if folder_exists and os.path.exists(url_path) \
            and os.path.exists(content_path) and os.path.exists(words_path):
        with open(content_path, 'r', encoding='utf8') as file:
            html = file.read()
        return get_urls(html)

    if not is_random:
        with urlopen(url) as response:
            content = response.read()
            curr_url = response.geturl()

    html = content.decode()

    # если URL-адрес новый, то файл с ним записывается
    if not folder_exists:
        try:
            os.mkdir(current_path)
        except FileExistsError:
            # если такое исключение произошло, то другой поток/процесс обрабатывает эту задачу
            return []
        with open(url_path, 'w', encoding='utf8') as file:
            file.write(curr_url)

    # если содержимое URL-адреса не существует, оно будет записано
    if not os.path.exists(content_path):
        with open(content_path, 'wb') as file:
            file.write(content)

    # если слова не были вычислены, то подчитываем их
    if not os.path.exists(words_path):
        hash_map = HashMap()
        count_words(html, hash_map)
        list_writer(hash_map.sort(), words_path)  # записывает все вычисленные слова в файл

    # получаем URL-адреса из статьи
    return get_urls(html)


if __name__ == '__main__':
    shutil.rmtree(ARTICLES_DIRECTORY)
    os.mkdir(ARTICLES_DIRECTORY)

    print('Parsing using multithreading')
    start = time.time()
    multi_parsing(WIKI_RANDOM, ThreadPoolExecutor, depth=1)
    print(time.time() - start)

    print(len(os.listdir(ARTICLES_DIRECTORY)))

    shutil.rmtree(ARTICLES_DIRECTORY)
    os.mkdir(ARTICLES_DIRECTORY)

    print('Parsing using multiprocessing')
    start = time.time()
    multi_parsing(WIKI_RANDOM, Pool, depth=1)
    print(time.time() - start)

    print(len(os.listdir(ARTICLES_DIRECTORY)))

    print('Merging')
    start = time.time()
    files_merge(*(f'{ARTICLES_DIRECTORY}/{folder}/words.txt'
                  for folder in os.listdir(ARTICLES_DIRECTORY)),
                result_path='res.txt')
    print(time.time() - start)
