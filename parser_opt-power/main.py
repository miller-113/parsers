import csv
import json
import random
import re
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from const import *

FILE_PATH_PARS = r'\\192.168.1.11\Volume_1\Price\opt_power\\'
# FILE_PATH_PARS = r'C:\Users\mille\Desktop\HW\\'
URL = 'https://opt-power.com.ua/'
URL_LOGIN = 'https://opt-power.com.ua/login'


def get_last_page():
    s = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s, options=Options())
    # browser.minimize_window()

    browser.get('https://opt-power.com.ua/login')
    log_in = browser.find_element(By.XPATH, '//*[@id="loginform-email"]')
    time.sleep(3)

    log_in.clear()

    log_in.send_keys(login)

    passwrd_in = browser.find_element(By.XPATH, '//*[@id="loginform-password"]')
    passwrd_in.clear()
    passwrd_in.send_keys(password)

    time.sleep(3)
    browser.find_element(By.PARTIAL_LINK_TEXT, '//*[@id="loginform"]/div[5]/div/button').click()

    browser.get('https://opt-power.com.ua/catalog?page=1000')
    time.sleep(5)
    last_page = browser.find_element(By.XPATH, '//*[@id="w0"]/div/ul/li[11]/a').text
    browser.close()
    return int(last_page)


def get_products_data():
    session = requests.Session()
    session.post(URL_LOGIN, data=json.dumps(data), headers=headers)
    product_data = []
    last_page = 130 #get_last_page()
    check = ''
    check1 = 0
    for page in tqdm(range(1, 1001)):
        response = session.get(url=f'https://opt-power.com.ua/catalog?page={page}', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        all_pr_on_page = soup.find('tbody').find_all('tr')
        if all_pr_on_page == check:
            check1 += 1
            if check1 > 5:
                break
            continue

        for pr in all_pr_on_page:
            prod_data = pr.find_all('td')
            try:
                id = prod_data[1].text
                name = prod_data[2].text
                stock = prod_data[3].text
                price = prod_data[5].text
                product_data.append({
                    'id': id,
                    'name': re.sub(r'\nNEW', '', name),
                    'stock': stock,
                    'price': price,
                })
            except Exception as e:
                print(e)
                continue
        time.sleep(random.randint(1, 2))
        # if len(all_pr_on_page) < 20:
        #     break
        check = all_pr_on_page
    return product_data


def csv_writer(path=FILE_PATH_PARS, file_name='testdata'):
    pr_data = get_products_data()

    with open(f'{path}{file_name}.csv', mode='w', newline='', encoding='utf8') as product_date:
        fieldnames = ['Ид', 'Название', 'Наличие', 'Цена', 'TY']
        product_date_writer = csv.DictWriter(product_date, fieldnames=fieldnames)
        product_date_writer.writeheader()

        for pr in pr_data:
            product_date_writer.writerow({'Ид': pr.get('id'), 'Название': pr.get('name'),
                                          'Наличие': pr.get('stock'), 'Цена': pr.get('price'),
                                          })

    return f'Создан {file_name} в {path}'


if __name__ == '__main__':
    print(csv_writer())

