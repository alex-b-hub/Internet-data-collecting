# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from hashlib import md5


class JobparserPipeline:


    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy1204

        # что делать если надо очистить базу данных?


    def id_hash(self, dict):
        '''Функция формирующая hash-строку из полученного словаря dict
        :param dict: полученного словаря dict
        :return result: hash-строка
        '''

        temp = str(dict).encode('utf-8')
        result = md5(temp).hexdigest()

        return result


    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min_salary'], item['max_salary'], item['currency'] = self.hh_process_salary(item['salary'])
            # del item['salary']
            item['company'] = self.hh_process_company(item['company'])
        elif spider.name == 'superjob':
            item['min_salary'], item['max_salary'], item['currency'] = self.sj_process_salary(item['salary'])
        else:
            print(f'unexpected spider name: {spider.name}')

        dict = [item['name'], item['url']]
        item['_id'] = self.id_hash(dict)   # формируем hash-строку из словаря dict

        collection = self.mongobase[spider.name]

        try:                               # записаны будут только данные с уникальнм _id
            collection.insert_one(item)
        except DuplicateKeyError:
            print(f"Document with id = {item['_id']} is already exists")

        return item


    def hh_process_salary(self, salary):
        temp_list = []
        for el in salary:
            el = el.replace(u'\xa0', u'')
            if el:
                temp_list.append(el)

        if temp_list[0] == 'от ' and temp_list[2] == ' до ':
            currency = temp_list[5]
            min_salary = int(temp_list[1])
            max_salary = int(temp_list[3])
        elif temp_list[0] == 'от ':
            currency = temp_list[3]
            min_salary = int(temp_list[1])
            max_salary = None
        elif temp_list[0] == 'до ':
            currency = temp_list[3]
            max_salary = int(temp_list[1])
            min_salary = None
        elif temp_list[0] == 'з/п не указана':
            currency = None
            min_salary = None
            max_salary = None
        else:
            print('unusual format of sallary')

        return min_salary, max_salary, currency


    def hh_process_company(self, company):
        if len(company) > 1:
            company = str(company[0] + company[1])
        else:
            company = str(company[0])

        return company


    def sj_process_salary(self, salary):
        temp_list = []
        for el in salary:
            el = el.replace(u'\xa0', u'')
            if el:
                temp_list.append(el)

        if temp_list[0] == 'от':
            currency = temp_list[1][-4:]
            min_salary = int(temp_list[1][:-4])
            max_salary = None
        elif temp_list[0] == 'до':
            currency = temp_list[1][-4:]
            max_salary = int(temp_list[1][:-4])
            min_salary = None
        elif temp_list[0] == 'По договорённости':
            currency = None
            min_salary = None
            max_salary = None
        elif temp_list[0].isdigit():
            currency = temp_list[3]
            min_salary = int(temp_list[0])
            max_salary = int(temp_list[2])
        else:
            print('unusual format of sallary')

        return min_salary, max_salary, currency

