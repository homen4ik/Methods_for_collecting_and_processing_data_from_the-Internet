# Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее
# авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide). Сделайте запрос,
# чтобы получить список всех сообществ на которые вы подписаны.

import json
import requests
from pprint import pprint


url = "https://api.vk.com/method/groups.get/?v=5.131&\
access_token=dc93f8530ad168d182734968d8ca78b24dde1596b711f65ef5bae607711d1f6a2bf1d5c2f4fde55263960"

response = requests.get(url)
my_group = response.json()

pprint(my_group)

with open('my_group.json', 'w') as f:
    json.dump(my_group, f)

