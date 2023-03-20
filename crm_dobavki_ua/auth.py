import requests
import fake_useragent
import time

session = requests.Session()

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}

url_catalog = 'https://crm.dobavki.ua/client/product/list/'
url_to_login = 'https://crm.dobavki.ua/client/login/?auth_redirect=/client/product/list/'

data = {
    'shopSiteLanguage': 'ru',
    'login': 'sup@foods-body.ua',
    'password': 'Z1dpKi3P',
    'ok': 'Войти в кабинет клиента'
}

log_in = session.post(url_to_login, headers=headers, data=data, params={'auth_redirect': '/client/product/list/'}).text

time.sleep(1)

# FILE_PATH_PARS = r'\\192.168.1.11\Volume_1\Price\crm_dobavki\\'
FILE_PATH_PARS = r'C:\Users\mille\Desktop\HW\\'
