# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД

from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
from datetime import date
import json
from pymongo.errors import DuplicateKeyError as dke

url = 'https://yandex.ru/news/'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'     
                         'Chrome/101.0.4951.67 Safari/537.36'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class, 'mg-card mg-card_')]")
data = date.today()
list_items = []
for item in items[:5]:

    item_info = {}
    name_resourse = item.xpath("..//span[@class='mg-card-source__source']//text()")
    name_resourse = str(name_resourse).replace('\xa0', ' ')

    name_news = item.xpath("..//h2[@class='mg-card__title']//text()")
    link_news = item.xpath("..//h2[@class='mg-card__title']/a/@href")
    time_publication = item.xpath("..//span[@class='mg-card-source__time']/text()")


    item_info['name_resourse'] = name_resourse
    item_info['name_news'] = name_news
    item_info['link_news'] = link_news
    item_info['data_publication'] = str(data) + str(time_publication)

    list_items.append(item_info)

pprint(list_items)

with open('news_yandex.txt', 'w') as f:
    json.dump(list_items, f)

client = MongoClient('127.0.0.1', 27017)
db = client['news_yandex']
news = db.news

with open('news_yandex.txt') as f:
    data = json.load(f)

for i in range(len(list_items)):
    try:
        news.insert_one(list_items[i])
    except dke:
        print(f'Новость {i} уже в базе')
