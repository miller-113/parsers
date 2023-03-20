import json
import re

import requests
import fake_useragent
import time
from bs4 import BeautifulSoup
import sys

import django
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.test import Client

session = requests.Session()

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}

url_catalog = 'https://dsn.com.ua/'
url_to_login = 'https://dsn.com.ua/security/login/'
client = requests.Session()

# cont1 = client.get(url_to_login, headers=headers).text
# cont = requests.get(url_to_login, headers=headers).text

cont = requests.get(url_catalog, headers=headers, allow_redirects=True)
csrf = re.findall(r'CSRFToken",type:\'hidden\'........(\w+)', str(cont.text))

# csrf = re.findall(r'CSRF_TOKEN: .(\w+)', str(cont))[0]

data = {
    'user[email]': 'sup@foods-body.ua',
    'user[pass]': 'qwerty56',
    'CSRFToken': csrf[1],
}
log_in = session.post(url_to_login, headers=dict(referer=url_to_login), data=data, allow_redirects=True)

time.sleep(1)

a = session.get('https://dsn.com.ua/zhirospaluvachi/', headers=headers)
with open('s.html', 'w', encoding='utf8') as f:
    f.write(str(a.text))
# FILE_PATH_PARS = r'\\192.168.1.11\Volume_1\Price\crm_dobavki\\'
# FILE_PATH_PARS = r'C:\Users\mille\Desktop\HW\\'
