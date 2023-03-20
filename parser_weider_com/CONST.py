import time

import fake_useragent
import os
import requests


FILE_PATH_PARS = os.path.join('//192.168.1.11/Volume_1/Прайсы/weider/')
FILE_PATH_MONITORING = os.path.join('//192.168.1.11/Volume_1/Прайсы/')

session = requests.Session()
user = fake_useragent.UserAgent().random
url_to_login = 'https://www.weider.com.ua/tools/login/'
headers = {'user-agent': user}

url_catalog = 'https://www.weider.com.ua/katalog/'

data = {
    'jsOnLoad': '',
    'action': 'login',
    'mode': 'login',
    'email': 'login',
    'password': 'password',
}

log_in = session.post(url_to_login, headers=headers, data=data).text
time.sleep(2)









