# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy2106

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary(item['salary'])
        else:
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_sj(item['salary'])

        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        if not salary:
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary = salary.getText()
            salary = re.split(r'\s|-', salary)
            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1]) * 1000
                currency = salary[3]
            elif salary[0] == 'от':
                salary_min = int(salary[1]) * 1000
                salary_max = None
                currency = salary[3]
            elif len(salary) < 5:
                salary_min = int(salary[0]) * 1000
                salary_max = int(salary[0]) * 1000
                currency = salary[2]
            else:
                salary_min = int(salary[0]) * 1000
                salary_max = int(salary[3]) * 1000
                currency = salary[5]
        return salary_min, salary_max, currency

    def process_salary_sj(self, salary):
        if salary == 'По договоренности' or '/месяц':
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary = salary.split('&nbsp;', salary)
            if salary[0] == 'от':
                salary_min = int(salary[1]) * 1000
                salary_max = None
                currency = salary[5]
            elif salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1]) * 1000
                currency = salary[3]
            elif len(salary) < 5:
                salary_min = int(salary[0]) * 1000
                salary_max = int(salary[0]) * 1000
                currency = salary[2]
            else:
                salary_min = int(salary[0]) * 1000
                salary_max = int(salary[3]) * 1000
                currency = salary[5]
        return salary_min, salary_max, currency





