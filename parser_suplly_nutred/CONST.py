import fake_useragent
import os
user = fake_useragent.UserAgent().random

FILE_PATH_PARS = os.path.join('C:/Users/mille/Desktop/HW/')
FILE_PATH_MONITORING = os.path.join('C:/Users/mille/Desktop/HW/')

headers = {
    'user-agent': user
}

data = {
    'mail': 'login',
    'pass': 'password',
    'login': 'true'
}

url_login = 'https://supply.nutrend.com.ua/'
url_pr_data = 'https://supply.nutrend.com.ua/index.php?page=catalog'