# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять
# только новые вакансии в вашу базу.


from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
import re
from pprint import pprint
import json


client = MongoClient('127.0.0.1', 27017)
db = client['hh0206']
vacancy = db.vacancy

with open('data.txt') as f:
    data = json.load(f)

db.vacancy.insert_many(data)

for vacancy_info in data:
    link = vacancy_info['link']
    id = re.split('/', link)[4]
    vacancy_info['_id'] = id[:8]

for i in range(len(data)):
    try:
        vacancy.insert_one(data[i])
        print(f'Вакансия {data[i]["name"]} добавлена')
    except dke:
        print(f'Вакансия {data[i]["name"]} уже существует')


# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).


salary = int(input("Введите необходимую зарплату: "))

for doc in vacancy.find({'$or': [{'salary_min': {'$gte': salary}}, {'salary_max': {'$gte': salary}}]}):
    pprint(doc)

