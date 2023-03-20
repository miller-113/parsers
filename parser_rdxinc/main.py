import csv
import random
import re
from auth import *
import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_products_data():
    PR_DATA = []
    url = 'https://rdxinc.com.ua/'
    dubl_check = []
    s = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s)
    browser.minimize_window()
    browser.get('https://www.google.com')

    request = session.get(url, headers=headers)
    soup = BeautifulSoup(request.content, 'lxml')
    drop_down_menu = soup.find('div',
                               class_='col-sm-12 col-md-3 menu-box hidden-xs hidden-sm'). \
        find_all('li', class_='dropdown')
    main_links = []
    for m_link in drop_down_menu:
        main_links.append(f"{url}{m_link.find('a').get('href')}")

    for link in tqdm(main_links):
        request = session.get(link, headers=headers)
        soup = BeautifulSoup(request.content, 'lxml')
        last_page = int(
            str(soup.find('div', class_='col-sm-12 text-center').find_all('a')[
                    -1].get('href')).split('=')[1])
        for page in range(1, last_page + 1):

            page_ = f'{link}?page={page}'
            request = session.get(page_, headers=headers)
            soup = BeautifulSoup(request.content, 'lxml')
            for y in soup.find_all('div', class_='product-name'):

                if y.find_parent().find('select') == None:

                    temp_url = y.find('a').get('href')
                    if temp_url not in dubl_check:
                        request = session.get(temp_url, headers=headers)
                        soup = BeautifulSoup(request.content, 'lxml')
                        soup.find('div', class_='info-product')
                        pr_link = temp_url
                        pr_qty = soup.find('div', class_='info-product').find(
                            'span').text.strip()
                        pr_id = soup.find('div',
                                          class_='info-product p-model').find(
                            'span').text
                        pr_id_additional = \
                            re.findall(
                                '<div class="info-product"><b>Артикул:</b> <span itemprop="sku">(\d+)</span></div>',
                                str(soup))
                        try:
                            pr_id_additional = pr_id_additional[0]
                        except:
                            pr_id_additional = pr_id_additional
                        pr_name = soup.find('h1', class_='h1-prod-name').text
                        pr_price = soup.find('div', class_='price').find(
                            'span').text.split()[0]
                        pr_old_price = '0'
                        if soup.find('span', class_='price-new') is not None:
                            pr_old_price = pr_price
                            pr_price = soup.find('span',
                                                 class_='price-new').text
                        pr_label = soup.find('div',
                                             class_='info-product p-brand').find(
                            'span').text
                        PR_DATA.append({
                            'link': pr_link,
                            'name': pr_name.replace(',', '.'),
                            'id': pr_id,
                            'qty': '?',
                            'qty1': pr_qty,
                            'price': pr_price,
                            'old_price': pr_old_price,
                            'label': pr_label,
                            'additional_id': pr_id_additional,

                        })
                        dubl_check.append(temp_url)
                else:
                    for i in enumerate(
                            y.find_parent().find('select').find_all('option')):
                        pr_link = i[1].get('data-href')
                        if pr_link not in dubl_check:

                            pr_id = i[1].get('data-model')
                            pr_size = i[1].text
                            pr_name = i[1].get('data-name')
                            pr_price = i[1].get('data-price').split('<')[0]
                            pr_old_price = '0'

                            if i[1].get('data-special') is not None:
                                pr_old_price = pr_price
                                pr_price = i[1].get('data-special').split('<')[
                                    0]

                            pr_qty = i[1].get('data-qty')
                            request = session.get(y.find('a').get('href'),
                                                  headers=headers)
                            soup = BeautifulSoup(request.text, 'lxml')
                            pr_label = soup.find('div',
                                                 class_='info-product p-brand').find(
                                'span').text
                            browser.get(y.find('a').get('href'))
                            share = browser.find_elements(By.CLASS_NAME,
                                                          'hpm-item')
                            share[i[0]].click()
                            time.sleep(0.2)
                            pr_id_additional = re.findall(
                                '<div class="info-product"><b>Артикул:</b> <span itemprop="sku">(\d+)</span></div>',
                                browser.page_source)

                            try:
                                pr_id_additional = pr_id_additional[0]
                            except:
                                pr_id_additional = pr_id_additional
                            PR_DATA.append({
                                'link': pr_link,
                                'name': str(pr_name).replace(',', '.'),
                                'id': pr_id,
                                'qty1': 'Есть в наличии' if int(
                                    pr_qty) > 0 else 'Нет в наличии',
                                'qty': pr_qty,
                                'price': pr_price,
                                'old_price': pr_old_price,
                                'label': pr_label,
                                'size': pr_size,
                                'additional_id': pr_id_additional,
                            })
                            dubl_check.append(pr_link)
            time.sleep(random.randint(1, 3))
    browser.close()
    return PR_DATA


def csv_writer(path=FILE_PATH_PARS, file_name='testdata3'):
    pr_data = get_products_data()

    with open(f'{path}{file_name}.csv', mode='w', newline='',
              encoding='utf8') as product_date:
        fieldnames = ['Название', 'Ссылка', 'Цена', 'Старая цена',
                      'НаличиеКолл.', 'Наличие', 'Бренд', 'Ид', 'Доп.Ид',
                      'Размер', 'TY']
        product_date_writer = csv.DictWriter(product_date,
                                             fieldnames=fieldnames)
        product_date_writer.writeheader()

        for pr in pr_data:
            product_date_writer.writerow(
                {'Название': pr.get('name'), 'Ссылка': pr.get('link'),
                 'Цена': pr.get('price'), 'Старая цена': pr.get('old_price'),
                 'НаличиеКолл.': pr.get('qty'), 'Бренд': pr.get('label'),
                 'Ид': pr.get('id'), 'Размер': pr.get('size'),
                 "Доп.Ид": pr.get("additional_id"), "Наличие": pr.get('qty1')
                 })

    return f'Создан {file_name} в {path}'


if __name__ == '__main__':
    print(csv_writer())
