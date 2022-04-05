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
# Собирать данные из нужного источника (см. выше).
# Для того, чтобы избежать реакции на частые обращения используется список актуальных User agent
# Данные записываются в итоговый файл, который затем можно обрабатывать не обращаясь к первоисточнику


# Список актуальных User agent по состоянию на 04.2022 для десктопных компьютеров взят из источника:
# http://web-data-extractor.net/faq/spisok-aktualnyx-user-agent/

# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36
# Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36
# Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36
# Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36
# Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36
# Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0
### Mozilla/5.0 (Macintosh; Intel Mac OS X 12.3; rv:98.0) Gecko/20100101 Firefox/98.0
# Mozilla/5.0 (X11; Linux i686; rv:98.0) Gecko/20100101 Firefox/98.0
# Mozilla/5.0 (Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0
# Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:98.0) Gecko/20100101 Firefox/98.0
# Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0
# Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0
# Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15
### Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)
### Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)
### Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)
### Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)
### Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)
### Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)
### Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)
# Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko
# Mozilla/5.0 (Windows NT 6.2; Trident/7.0; rv:11.0) like Gecko
# Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
### Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/99.0.1150.36
# Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/99.0.1150.36
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 OPR/85.0.4341.18
# Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 OPR/85.0.4341.18
# Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 OPR/85.0.4341.18
### Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 OPR/85.0.4341.18
# Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Vivaldi/4.3
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Vivaldi/4.3
# Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Vivaldi/4.3
### Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Vivaldi/4.3
### Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Vivaldi/4.3
# Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 YaBrowser/22.3.0 Yowser/2.5 Safari/537.36
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 YaBrowser/22.3.0 Yowser/2.5 Safari/537.36
# Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 YaBrowser/22.3.0 Yowser/2.5 Safari/537.36


# ОТКУДА БЕРЕМ ДАННЫЕ
#https://hh.ru/search/vacancy?text=Python&area=113&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=true&page=0&hhtmFrom=vacancy_search_list

import requests

# список User agent (пока подготовил вручную (цейтнот), на будущее можно и автоматически соскрапить)
user_agent_list = ['Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Vivaldi/4.3',
                   'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.3; rv:98.0) Gecko/20100101 Firefox/98.0',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 OPR/85.0.4341.18',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
                   'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                   'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
                   'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'
                   ]

i = 0
max = 2 #количество страниц в hh.ru с данными (цейтнот: задаем вручную) !!! НЕ БОЛЕЕ 100
for n in range(0, max):
    url = 'https://hh.ru/search/vacancy?text=Python&area=113&salary=&currency_code=RUR&experience=' \
          'doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&no_magic=true&L_save_area=' \
          'true&page=' + str(n) + '&hhtmFrom=vacancy_search_list'

    if n > 10:
        i = n - 10 * n//10

    headers = {'User-agent': user_agent_list[i]}

    response = requests.get(url, headers=headers)

    if response.ok:
        with open('response_hh.html', 'a', encoding='utf-8') as f: # данные записываются в итоговый файл
            f.write(response.text)

