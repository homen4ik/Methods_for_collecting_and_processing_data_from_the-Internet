# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com/users/homen4ik/repos'

response = requests.get(url)

repo_list = []

for repo in response.json():
    if not repo['private']:
        repo_list.append(repo['name'])
        print(f"{repo['name']}")


with open('repo_list.json', 'w') as f:
    json.dump(repo_list, f)
