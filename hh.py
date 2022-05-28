# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
# одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.
# Сохраните в json либо csv.

# https://hh.ru/search/vacancy?area=232&experience=noExperience&search_field=name&text=аналитик&
# order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true


from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import pandas as pd


main_url = 'https://hh.ru'

page = 0

params = {'area': '232',
          'experience': 'noExperience',
          'search_field': 'name',
          'text': 'Аналитик',
          'order_by': 'relevance',
          'search_period': '0',
          'items_on_page': '20',
          'no_magic': 'true',
          'page': page,
          'L_save_area': 'true'}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'     
                         'Chrome/101.0.4951.67 Safari/537.36'}
response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)

all_vacancys = []

while True:

    html = response.text
    soup = bs(html, 'html.parser')

    vacancys = soup.find_all('div', {'class': 'vacancy-serp-item'})


    for vacancy in vacancys:
        vacancy_info = {}

        vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).getText()
        vacancy_link = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']

        salary_anchor = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary_anchor:
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary = salary_anchor.getText()

            salary = re.split(r'\s|-', salary)

            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1]) * 1000
                currency = salary[3]
            elif salary[0] == 'от':
                salary_min = int(salary[1]) * 1000
                salary_max = None
                currency = salary[3]
            else:
                salary_min = int(salary[0]) * 1000
                salary_max = int(salary[3]) * 1000
                currency = salary[5]

        vacancy_info['name'] = vacancy_name
        vacancy_info['link'] = vacancy_link
        vacancy_info['salary_min'] = salary_min
        vacancy_info['salary_max'] = salary_max
        vacancy_info['currency'] = currency
        vacancy_info['website'] = 'https://hh.ru'

        all_vacancys.append(vacancy_info)


    next_page = soup.find('a', {'data-qa': 'pager-next'})
    if next_page is None:
        break
    else:
        page += 1
        response = requests.get(main_url + next_page['href'], headers=headers)


#    pprint(all_vacancys)

    df_vacancy = pd.DataFrame(data=all_vacancys)
    df_vacancy.to_csv('hh_search.csv', index=False)

