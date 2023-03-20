import csv
import random
import time
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import fake_useragent

FILE_PATH_PARS = None


def get_data():
    pr_data = []
    PR_URLS = []
    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}

    s = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    browser = webdriver.Chrome(service=s, options=options)
    browser.set_window_size(1600, 1100)

    MAIN_URL = 'https://dsn.com.ua/'

    browser.get(MAIN_URL)
    browser.find_element(By.XPATH,
                         '/html/body/div[2]/div[1]/div/div[3]/div/div/div[2]/div/div/div').click()

    login_form = browser.find_element(By.XPATH,
                                      '//*[@id="login_form_id"]/dl/dd[1]/input')
    login_form.clear()
    login_form.send_keys('login')

    password_form = browser.find_element(By.XPATH,
                                         '//*[@id="login_form_id"]/dl/dd[2]/input')
    password_form.clear()
    password_form.send_keys('password')

    browser.find_element(By.XPATH,
                         '//*[@id="login_form_id"]/dl/dd[3]/span[1]/input').click()

    time.sleep(1)
    sele_cookies = browser.get_cookies()

    browser.close()

    session = requests.Session()
    # добавляем только те куки которые нужны
    cookies_dict = [
        {'domain': key.get('domain'), 'name': key.get('name'),
         'path': key.get('path'),
         'secure': key.get('secure'), 'value': key.get('value')}
        for key in sele_cookies
    ]
    # распаковка куки в сессию
    for cookies in cookies_dict:
        session.cookies.set(**cookies)

    # собираем ссылки на каталоги
    request = session.get(MAIN_URL, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')
    links = [MAIN_URL[:-1] + i.find('a').get('href') + 'filter/page=all/' for i
             in
             soup.find_all('div', class_='productsMenu-submenu __fluidGrid')[
                 1].find_all('li')]

    for link in links:
        request = session.get(link, headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')
        all_product_on_page = soup.find('tbody').find_all('tr')
        for product in all_product_on_page:
            if f"{MAIN_URL[:-1]}{product.find('a').get('href')}" not in PR_URLS:
                PR_URLS.append(
                    f"{MAIN_URL[:-1]}{product.find('a').get('href')}")
            else:
                continue

    for url in tqdm(PR_URLS):
        try:
            request = session.get(url,
                                  headers=headers)  # фикс стоит на 1 ссылку
            soup = BeautifulSoup(request.text, 'lxml')

            name = soup.find('div',
                             class_='product-header__block product-header__block--wide').text.strip()
            articul = soup.find_all('div', class_='product-header__block')[
                1].text.strip().split()[1]
            stock = soup.find('div',
                              class_='product-header__availability').text.strip().split()[
                -1]
            brand = soup.find('nav', class_='breadcrumbs').find_all('div')[
                3].text.strip()

            in_stock = stock if stock.isdigit() else '0'
            price = soup.find('div', class_='product-price__item').text.strip()
            price_rrc = soup.find('div', class_='hint').text.strip().split(':')[
                -1].strip()
            # здесь поставим проверку на дубликат если будет проблема
            pr_data.append({
                'name': name,
                'articul': articul,
                'brand': brand,
                'in_stock': in_stock,
                'price': price,
                'price_rrc': price_rrc,
                'url': url,
            })
        except Exception as e:
            print(f'Error with {url}', e)
            continue
    time.sleep(random.uniform(0.5, 1.5))

    return sorted(pr_data, key=lambda x: x['brand'])


def csv_writer(path=FILE_PATH_PARS, file_name='testdata'):
    pr_data = get_data()

    with open(f'{path}{file_name}.csv', mode='w', newline='',
              encoding='utf8') as product_date:
        fieldnames = ['Название', 'Артикул', 'Бренд', 'Наличие', 'Цена',
                      'Цена РРЦ', 'Ссылка', 'TY']
        product_date_writer = csv.DictWriter(product_date,
                                             fieldnames=fieldnames)
        product_date_writer.writeheader()

        for pr in pr_data:
            product_date_writer.writerow(
                {'Название': pr.get('name'), 'Артикул': pr.get('articul'),
                 'Бренд': pr.get('brand'), 'Наличие': pr.get('in_stock'),
                 'Цена': pr.get('price'), 'Цена РРЦ': pr.get('price_rrc'),
                 'Ссылка': pr.get('url'),
                 })

    return f'Создан {file_name} в {path}'
