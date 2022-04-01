# Домашнее задание к уроку №1. "Основы клиент-серверного взаимодействия. Работа с API"

# 1. Посмотреть документацию к API GitHub, разобраться как вывести список наименований
# репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

#https://unetway.com/blog/sozdanie-tokena-personalnogo-dostupa-dla-komandnoj-stroki

#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

url = 'https://api.github.com/user/repos'
token = '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'
github_user_name = 'Aleksei Bakeev'

response = requests.get(url, auth=(github_user_name, token))

if response.ok:
    j_data = response.json()
    repositories = []
    print(f'User {github_user_name} has next repositories:')
    i = 0
    for rep in j_data:
        i += 1
        print(f"{i} {rep['name']}")
        repositories.append({i: rep['name']})
else:
    print(f'Error {response.status_code}')

with open('j_repositories.json', 'w') as file:
    json.dump(repositories, file)
