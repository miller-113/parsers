import time

import fake_useragent
import os
import requests

FILE_PATH_PARS = os.path.join('//192.168.1.11/Volume_1/Price/rdxinc/')
FILE_PATH_MONITORING = os.path.join('//192.168.1.11/Volume_1/Price/')

session = requests.Session()
user = fake_useragent.UserAgent().random
url_to_login = 'https://rdxinc.com.ua/index.php?route=common/login_modal/login_validate'
headers = {'user-agent': user}

url_catalog = 'https://rdxinc.com.ua/index.php?route=account/login'

data = {}
# data = {


log_in = session.post(url_to_login, headers=headers, data=data,
                      params={'route': 'account/login'}).text
time.sleep(2)
