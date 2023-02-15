import re

import requests
from bs4 import BeautifulSoup


def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.findAll('article', id='maincontent')[0]
    content = content.get_text()
    content = content.split("<<")[0]
    content = re.sub("^\s+|\n|\r|\s+$", '', content)
    return content


def parse_horoscope_for_zodiac(zodiac, day):
    url = f'https://uznayvse.ru/goroskop/{zodiac}-all-{day}.html'
    content = get_content(url)
    return content


def parse_horoscope_for_all(day):
    url = f'https://uznayvse.ru/goroskop/all-{day}.html'
    content = get_content(url)
    content = content.replace('Выберите свой знак:ОвенТелецБлизнецыРакЛевДеваВесыСкорпионСтрелецКозерогВодолейРыбы', '')
    return content


def parse_horoscope_compatibility(he, she):
    url = f'https://uznayvse.ru/goroskop/zhenshina-{she}-muzhchina-{he}-sovmestimost-znaka-zodiaka.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.findAll('div', class_='maincontent')[0]
    title_1 = 'Как женщине-'
    title_2 = 'Как мужчине-'
    result_content = []
    for data in content:
        data_g = re.sub("^\s+|\n|\r|\s+$", '', data.get_text())
        if len(data_g) != 0:
            if data_g.startswith('Каким будет союз мужчины-'):
                continue
            elif data_g.startswith('Какая девушка нужна мужчине-'):
                continue
            elif data_g.startswith('Какой мужчина подходит женщине-'):
                continue
            elif data_g == 'Достоинства союза':
                break
            if data_g.startswith(title_1):
                result_content.append(f'\n❤️{data_g}❤️\n')
            elif data_g.startswith(title_2):
                result_content.append(f'\n❤️{data_g}❤️\n')
            else:
                result_content.append(f'\n{data_g}\n')
    return result_content


# parse_horoscope_compatibility('oven', 'rak')
