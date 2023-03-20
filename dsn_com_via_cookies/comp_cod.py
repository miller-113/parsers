import csv
import datetime
import itertools
import os
from tqdm import tqdm

FILE_PATH_MONITORING = r'\\192.168.1.11\Volume_1\Price\\'


def read_csv(file_name):
    result = []
    with open(f'{file_name}', encoding='utf8') as f1:
        reader = csv.reader(f1)
        for row in reader:
            result.append(row)
    return result


def checker_for_new_n_modified(old_file, new_file,
                               monitoring_file='monitoringdata',
                               path=FILE_PATH_MONITORING):
    old = read_csv(old_file)
    new = read_csv(new_file)
    lst_new_pr = []
    lst_modified_pr = []
    lst_deleted_pr = []
    temp = set()
    temp1 = set()
    new_: str
    old_: str
    for old_ in tqdm(old):
        for new_ in new:

            if new_[1] == old_[1]:
                if new_[5] != old_[5] or new_[4] != old_[4] or str(
                        new_[3]) == '0' and str(old_[3]) != '0' or str(
                        new_[3]) != '0' and str(old_[3]) == '0':
                    lst_modified_pr.append({
                        'OLD': old_, 'NEW': new_
                    })
            temp1.add(old_[1])
            temp.add(new_[1])

    lst_modified_pr, lst_modified_pr = sorted(lst_modified_pr,
                                              key=lambda x: x.get('NEW')[2]), \
        sorted(lst_modified_pr, key=lambda x: x.get('OLD')[2])

    attr_id_prod = temp - temp1
    attr_id_prod1 = temp1 - temp

    for products in new:
        for id_prod in attr_id_prod:
            if id_prod == products[1]:
                lst_new_pr.append(products)
    lst_new_pr = sorted(lst_new_pr, key=lambda x: x[2])
    for products in old:
        for id_prod in attr_id_prod1:
            if id_prod == products[1]:
                lst_deleted_pr.append(products)
    lst_deleted_pr = sorted(lst_deleted_pr, key=lambda x: x[2])

    if len(lst_new_pr) > 0 or len(lst_modified_pr) > 0 or len(
            lst_deleted_pr) > 0:
        with open(f'{path}{monitoring_file}.csv', 'w', encoding='utf8',
                  newline='') as file:
            fieldnames = ['Название', 'Артикул', 'Бренд', 'Наличие', 'Цена',
                          'Цена РРЦ', 'Ссылка', 'Изменения']
            w = csv.DictWriter(file, fieldnames=fieldnames)

            if len(lst_modified_pr) > 0:
                w.writeheader()
                for fields in range(len(lst_modified_pr)):
                    ch = 0
                    str_attr = ''
                    ch += 1
                    if str(lst_modified_pr[fields].get('OLD')[3]) != str(
                            lst_modified_pr[fields].get('NEW')[3]) and \
                            ch == 1:
                        str_attr += 'Наличие'
                    if str(lst_modified_pr[fields].get('OLD')[4]) != str(
                            lst_modified_pr[fields].get('NEW')[4]) and \
                            ch == 1:
                        str_attr += 'Цена'
                    if str(lst_modified_pr[fields].get('OLD')[5]) != str(
                            lst_modified_pr[fields].get('NEW')[5]) and \
                            ch == 1:
                        str_attr += 'Цена(РРЦ)'
                    w.writerow({
                        'Название': lst_modified_pr[fields].get('NEW')[0],
                        'Артикул': lst_modified_pr[fields].get('NEW')[1],
                        'Бренд': lst_modified_pr[fields].get('NEW')[2],
                        'Наличие': lst_modified_pr[fields].get('NEW')[3],
                        'Цена': lst_modified_pr[fields].get('NEW')[4],
                        'Цена РРЦ': lst_modified_pr[fields].get('NEW')[5],
                        'Ссылка': lst_modified_pr[fields].get('NEW')[6],
                        'Изменения': str_attr,
                    }
                    )

            if len(lst_new_pr) > 0:
                w.writeheader()
                for data in lst_new_pr:
                    w.writerow({
                        'Название': data[0],
                        'Артикул': data[1],
                        'Бренд': data[2],
                        'Наличие': data[3],
                        'Цена': data[4],
                        'Цена РРЦ': data[5],
                        'Ссылка': data[6],
                        'Изменения': 'Новые товары'})
            if len(lst_deleted_pr) > 0:
                w.writeheader()
                for data in lst_deleted_pr:
                    w.writerow({
                        'Название': data[0],
                        'Артикул': data[1],
                        'Бренд': data[2],
                        'Наличие': data[3],
                        'Цена': data[4],
                        'Цена РРЦ': data[5],
                        'Ссылка': data[6],
                        'Изменения': 'Удаленные'})

        return f'Файл {monitoring_file} создан в {path}'
    else:
        return f'Изменений не найдено'
