import csv
import random
import re
from auth import *
from bs4 import BeautifulSoup
import time
import xlsxwriter
import pandas as pd


def get_data():
    pr_data = []

    pagination = 0
    while True:
        request = session.get(
            f'https://crm.dobavki.ua/client/product/list/?page={pagination}',
            headers=headers)
        soup = BeautifulSoup(request.content, 'lxml')
        try:
            all_products_on_page = soup.find('div',
                                             class_='os-overflow-table standalone js-product-table').find_all(
                'tr')
            for product_data in all_products_on_page[1:]:
                product_data = product_data.find_all('td')
                id_ = product_data[1].text
                name_ = re.split(r'\s{2,99}', product_data[2].get_text())[1]
                brand_ = product_data[3].text.strip()
                bar_code_ = product_data[4].text.strip()
                stock_ = product_data[5].text.strip()
                price_ = product_data[6].text.strip()
                bb_date_ = product_data[7].text.strip()
                pr_data.append({
                    'id': id_,
                    'name': name_,
                    'brand': brand_,
                    'bar_code': bar_code_,
                    'stock': stock_,
                    'price': price_,
                    'bb_date': bb_date_,
                })
            time.sleep(random.randint(1, 1))
            pagination += 1
            if soup.find('div', class_='ob-block-stepper').find_all('a')[
                -1].text.isdigit():
                break
        except Exception as e:
            print(e)
            continue
    return pr_data


def csv_writer(path=FILE_PATH_PARS, file_name='testdata'):
    pr_data = get_data()

    with open(f'{path}{file_name}.csv', mode='w', newline='',
              encoding='utf8') as product_date:
        fieldnames = ['Ид', 'Название', 'Бренд', 'Штрих код', 'Наличие', 'Цена',
                      'Срок годности', 'TY']
        product_date_writer = csv.DictWriter(product_date,
                                             fieldnames=fieldnames)
        product_date_writer.writeheader()

        for pr in pr_data:
            product_date_writer.writerow(
                {'Ид': pr.get('id'), 'Название': pr.get('name'),
                 'Бренд': pr.get('brand'), 'Штрих код': pr.get('bar_code'),
                 'Наличие': pr.get('stock'), 'Цена': pr.get('price'),
                 'Срок годности': pr.get('bb_date'),
                 })

    return f'Создан {file_name} в {path}'


if __name__ == '__main__':
    print(csv_writer())
