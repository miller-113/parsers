import fake_useragent


user = fake_useragent.UserAgent().random
login = 'sup@foods-body.ua'
password = 'qwerty56'
headers = {'user-agent': user}

data = {
    'password': password,
    'email': login,
}
