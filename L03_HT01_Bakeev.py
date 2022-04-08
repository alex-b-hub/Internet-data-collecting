# Домашнее задание к уроку №3 "Система управления базами данных MongoDB в Python"
# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.
# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).


from bs4 import BeautifulSoup as bs
#import requests
from pprint import pprint
import re
import json
#from bson import ObjectId
from pymongo import MongoClient
from hashlib import md5
from pymongo.errors import DuplicateKeyError


# ------------------------------------------------------
# Функция формирующая hash-строку из полученного словаря dict
def id_hash(dict):
    temp = str(dict).encode('utf-8')
    result = md5(temp).hexdigest()

    return result


# -------------------------------------------------------------------------------------------------------
# Функция готовящая словарь с данными о вакансии из полученного DOM и записывающая его в базу данных base
def job_dict_insert(dom, base):

    jobs = dom.find_all('div', {'class': 'vacancy-serp-item'})
    counter = 0
    add_num = 0
    error_num = 0

    jobs_list = []
    for j in jobs:
        counter += 1
        j_wage_min = None
        j_wage_max = None
        j_wage_currency = None
        j_data = {}
        j_link = j.find('a', {'class': 'bloko-link'})['href']
        j_name = j.find('a', {'class': 'bloko-link'}).getText()
        wage = j.find('span', {'class': 'bloko-header-section-3'})
        if wage:
            wage = wage.getText().replace(u'\u202f', u'')
            j_wage_currency = wage[len(wage) - 4:len(wage)].replace(' ', '')
            wage_figures = wage[:-4]
            if wage_figures.find('от') >= 0:
                j_wage_min = int(re.sub(r'[^0-9]', '', wage_figures))
            elif wage_figures.find('до') >= 0:
                j_wage_max = int(re.sub(r'[^0-9]', '', wage_figures))
            else:
                wages = wage_figures.split("–")
                wages[0] = re.sub(r'[^0-9]', '', wages[0])
                j_wage_min = int(wages[0])
                if len(wages) > 1:
                    wages[1] = re.sub(r'[^0-9]', '', wages[1])
                    j_wage_max = int(wages[1])
                else:
                    j_wage_max = None

        else:
            j_wage_min = None
            j_wage_max = None
            j_wage_currency = None

        j_data['wage_min'] = j_wage_min
        j_data['wage_max'] = j_wage_max
        j_data['wage_currancy'] = j_wage_currency
        j_data['link'] = j_link
        j_data['name'] = j_name

        j_data['_id'] = id_hash(j_data)

        jobs_list.append(j_data)

        try:
            base.insert_one(j_data)
            add_num += 1
        except DuplicateKeyError:
            error_num += 1
            # print(f"Document with id = {j_data['_id']} already exists")

    # pprint(jobs_list)
    print(f'{counter} вакансий из "dom" было обработано')
    print(f'{add_num} вакансий было добавлено в базу данных {base}')
    print(f'{error_num} вакансий уже есть в базе данных {base}')

# -----------------------------------------------------------------------------------
# Функция формирующая выборку из полученной БД вакансий с уровнем зарплаты выше level
def job_selection(base, level):
    job_selection_list = []

    # обработка вакансий с зарплатой номинированной в рублях
    request = {'$or': [{'wage_min': {'$gte': level}}, {'wage_max': {'$gte': level}}]}
    for doc in base.find(request):
        job_selection_list.append(doc)
        #pprint(doc)

    # обработка вакансий с зарплатой номинированной в долларах
    level_usd = level / 75
    request = {'$and': [{'wage_currancy': {'$eq': 'USD'}},
                        {'$or': [{'wage_min': {'$gte': level_usd}}, {'wage_max': {'$gte': level_usd}}]}]}
    for doc in base.find(request):
        job_selection_list.append(doc)
        #pprint(doc)

    # обработка вакансий с зарплатой номинированной в евро
    level_euro = level / 85
    request = {'$and': [{'wage_currancy': {'$eq': 'EUR'}},
                        {'$or': [{'wage_min': {'$gte': level_euro}}, {'wage_max': {'$gte': level_euro}}]}]}
    for doc in base.find(request):
        job_selection_list.append(doc)
        #pprint(doc)

    with open('job_selection.json', 'w', encoding='utf-8') as file:
        json.dump(job_selection_list, file)


### --- ТЕЛО ОСНОВНОЙ ПРОГРАММЫ  ---

### подключаем Mongo и работаем с базой данных 'jobs_db'
client = MongoClient('127.0.0.1', 27017)
db = client['jobs_db']
vacancy = db.vacancy
#vacancy.delete_many({})    # если надо очистить базу данных

### считываем файл 'response_hh.html' и формируем dom с данными из этого файла
response = ''
with open('response_hh.html', 'r', encoding='utf-8') as f:
#with open('response.html', 'r', encoding='utf-8') as f:  # этот короткий файл хорош при отладке
    response = f.read()

dom = bs(response, 'html.parser')

### инициируем работу функции job_dict_inser, которая обрабатывает данные из dom и записывает в 'jobs_db'
job_dict_insert(dom, vacancy)

### инициируем работу функции job_selection, которая выбирает вакансии из 'jobs_db' с зарплатой выше level и записывает в 'job_selection.json'
level = 550000  # уровень зарплаты в рублях, который будет точкой отсечения
job_selection(vacancy, level)




