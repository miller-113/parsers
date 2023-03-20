import csv
import requests
from bs4 import BeautifulSoup
import warnings
from CONST import *

session = requests.Session()


def get_data(file_name, file_path=FILE_PATH_PARS):
    product_list = []
    response = session.post(url_login, headers=headers, data=data).text
    r = session.get(url_pr_data, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'id': 'price'}).find('tbody').find_all('tr')
    for pr in table:
        k = pr.find_all('td')
        if len(pr) > 1:
            product_list.append({'Код': k[0].text, "Название": k[1].text,
                                 "Размер": ''.join(
                                     [i for i in k[2].text if i != u'\xa0']),
                                 'Цвет': ''.join(
                                     [i for i in k[3].text if i != u'\xa0']),
                                 "Цена евро": ''.join([i for i in k[4].text if
                                                       i != u'\xa0']).split(
                                     '(')[0],
                                 "Цена грн": ''.join([i for i in k[4].text if
                                                      i != u'\xa0']).split('(')[
                                     1].replace(')', ''),
                                 'Наличие': 'В наличии' if k[5].text == '' else
                                 k[5].text})

    with open(f'{file_path}{file_name}.csv', mode='w', newline='',
              encoding='utf8') as product_date:
        fieldnames = ['Код', 'Название', 'Размер', 'Цвет', 'Цена евро',
                      'Цена грн', 'Наличие', 'TY']
        product_date_writer = csv.DictWriter(product_date,
                                             fieldnames=fieldnames)
        product_date_writer.writeheader()
        name_check = ''
        counter = 1
        for pr in product_list:
            product_date_writer.writerow(
                {'Код': pr.get('Код'), 'Название': pr.get('Название'),
                 'Размер': pr.get('Размер'), 'Цвет': pr.get('Цвет'),
                 'Цена евро': pr.get('Цена евро'),
                 'Цена грн': pr.get('Цена грн'),
                 'Наличие': pr.get('Наличие')})
    return f'Файл {file_name} создан в {file_path}'
