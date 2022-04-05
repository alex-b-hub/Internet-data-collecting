# Домашнее задание к уроку 2. Парсинг HTML. Библиотека Beautiful soup.
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
# с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#   1 Наименование вакансии.
#   2 Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
#   3 Ссылку на саму вакансию.
#   4 Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.


# ЗАДАЧА ЭТОЙ ПРОГРАММЫ
# обработать данные из файла response_hh.html в соответствии в ТЗ (см. выше)

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import json

# url = 'https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&text=Python&from=suggest_post&page=0&hhtmFrom=vacancy_search_list'
# headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

# we read data from response_hh.html
# response_hh.html - prepared file with parsered data from https://hh.ru/
response = ''
with open('response_hh.html', 'r', encoding='utf-8') as f:
#with open('response.html', 'r', encoding='utf-8') as f:  # this short file is useful in debugging
    response = f.read()

dom = bs(response, 'html.parser')

jobs = dom.find_all('div', {'class': 'vacancy-serp-item'})

jobs_list = []
for j in jobs:
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
            #print('_', wage_figures)
            j_wage_min = int(re.sub(r'[^0-9]', '', wage_figures))
        elif wage_figures.find('до') >= 0:
            #print('__', wage_figures)
            j_wage_max = int(re.sub(r'[^0-9]', '', wage_figures))
        else:
            #print('___', wage_figures)
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

    jobs_list.append(j_data)

#pprint(jobs_list)
print(f'{len(jobs_list)} vacancies have been processed')

with open('json_jobs_hh.json', 'w') as file:
    json.dump(jobs_list, file)