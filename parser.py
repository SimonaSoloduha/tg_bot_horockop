import re
import requests
from bs4 import BeautifulSoup


def remove_last_sentence(paragraph):
    """
    Удаление последнего предложения
    :param paragraph: str, параграф, в котором нужно удалить последнее пердложение
    :return: str, новый параграф
    """
    sentence_pattern = r'[^.!?]+[.!?]'
    sentences = re.findall(sentence_pattern, paragraph)

    if len(sentences) > 1:
        updated_paragraph = ' '.join(sentences[:-1])
        return updated_paragraph
    else:
        return ""


def get_content(url):
    """
    Функция забирает с сайта необходимый контент с помощью BeautifulSoup
    :param url: str
    :return: объект BeautifulSoup
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.findAll('article', id='maincontent')[0]
    content = content.get_text()
    content = re.sub("^\s+|\n\n|\t\t|\r\r|\s+$", '', content)
    return content


def parse_horoscope_for_zodiac(zodiac, day):
    """
    Парсер для гороскопа на 1 день для 1 знака зодиака
    :param zodiac: str
    :param day: str
    :return: str
    """
    url = f'https://uznayvse.ru/goroskop/{zodiac}-all-{day}.html'
    content = get_content(url)
    content = remove_last_sentence(content)
    content = content.replace('Мужчина', 'Мужчина 🐴')
    content = content.replace('Женщина', 'Женщина 🦄')
    return content


def parse_horoscope_for_all(day):
    """
    Парсер для гороскопа на 1 день для всех знаков
    :param day: str
    :return: str
    """
    url = f'https://uznayvse.ru/goroskop/all-{day}.html'
    content = get_content(url)
    content = content.split('Подробнее')
    content_text = ''

    for i in content:
        updated_paragraph = remove_last_sentence(i)
        updated_paragraph = updated_paragraph.replace('гороскоп на сегодня', '\t\n')
        if updated_paragraph:
            content_text += f'\t\n🔮{updated_paragraph}\t\n'
    return content_text


def parse_horoscope_compatibility(he, she):
    """
    Парсер для гороскопа на совместимость знаков
    :param he: str
    :param she: str
    :return: list
    """
    url = f'https://uznayvse.ru/goroskop/zhenshina-{she}-muzhchina-{he}-sovmestimost-znaka-zodiaka.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.findAll('div', class_='maincontent')[0]
    title_1 = 'Как женщине-'
    title_2 = 'Как мужчине-'
    result_content = []
    for data in content:
        data_g = re.sub("^\s+|\n|\r|\s+$", '', data.get_text())
        if len(result_content) < 12:
            if len(data_g) != 0:
                if data_g.startswith(title_1) or data_g.startswith(title_2):
                    result_content.append(f'\nТак что имей это ввиду 🧐\n')
                    break
                else:
                    result_content.append(f'\n{data_g}\n')
        else:
            result_content.append(f'\nТак что имей это ввиду 🧐\n')
            break
    return result_content
