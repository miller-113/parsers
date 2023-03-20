import csv
import datetime
import itertools
import os
from CONST import *
import sqlite3


def read_csv(file_name, file_path=FILE_PATH_PARS):
    result = []
    with open(f'{file_path}{file_name}', encoding='utf8') as f1:
        reader = csv.reader(f1)
        for row in reader:
            result.append(row)
    return result


def checker_for_new_n_modified(old_file, new_file, monitoring_file,
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
    for old_, new_ in itertools.product(old, new):
        count = 0

        # if new_ not in old:
        if new_[0] == old_[0]:
            if new_[1] != old_[1] or new_[2] != old_[2] or new_[3] != old_[3] or \
                    new_[4] != old_[4] \
                    or new_[6] != old_[6]:
                lst_modified_pr.append({
                    'OLD': old_, 'NEW': new_
                })
        temp1.add(old_[0])
        temp.add(new_[0])

    attr_id_prod = temp - temp1
    attr_id_prod1 = temp1 - temp
    # ищем новые товары
    for products in new:
        for id_prod in attr_id_prod:
            if id_prod == products[0]:
                lst_new_pr.append(products)

    for products in old:
        for id_prod in attr_id_prod1:
            if id_prod == products[0]:
                lst_deleted_pr.append(products)

    if len(lst_new_pr) > 0 or len(lst_modified_pr) > 0 or len(
            lst_deleted_pr) > 0:
        with open(f'{path}{monitoring_file}.csv', 'w', encoding='utf8',
                  newline='') as file:
            fieldnames = ['Код', 'Название', 'Размер', 'Цвет', 'Цена евро',
                          'Цена грн', 'Наличие', 'Изменения']
            w = csv.DictWriter(file, fieldnames=fieldnames)

            if len(lst_modified_pr) > 0:
                w.writeheader()
                for fields in range(len(lst_modified_pr)):
                    ch = 0
                    str_attr = ''
                    ch += 1
                    if str(lst_modified_pr[fields].get('OLD')[1]) != str(
                            lst_modified_pr[fields].get('NEW')[1]) and \
                            ch == 1:
                        str_attr += 'Название'
                    if str(lst_modified_pr[fields].get('OLD')[2]) != str(
                            lst_modified_pr[fields].get('NEW')[2]) and \
                            ch == 1:
                        str_attr += 'Размер'
                    if str(lst_modified_pr[fields].get('OLD')[3]) != str(
                            lst_modified_pr[fields].get('NEW')[3]) and \
                            ch == 1:
                        str_attr += 'Цвет'
                    if str(lst_modified_pr[fields].get('OLD')[4]) != str(
                            lst_modified_pr[fields].get('NEW')[4]) and \
                            ch == 1:
                        str_attr += 'Цена евро'
                    if str(lst_modified_pr[fields].get('OLD')[6]) != str(
                            lst_modified_pr[fields].get('NEW')[6]) and \
                            ch == 1:
                        str_attr += 'Наличие'
                    w.writerow({'Код': lst_modified_pr[fields].get('NEW')[0],
                                'Название': lst_modified_pr[fields].get('NEW')[
                                    1],
                                'Размер': lst_modified_pr[fields].get('NEW')[2],
                                'Цвет': lst_modified_pr[fields].get('NEW')[3],
                                'Цена евро': lst_modified_pr[fields].get('NEW')[
                                    4],
                                'Цена грн': lst_modified_pr[fields].get('NEW')[
                                    5],
                                'Наличие': lst_modified_pr[fields].get('NEW')[
                                    6],
                                'Изменения': str_attr,
                                }
                               )
            if len(lst_new_pr) > 0:
                w.writeheader()
                for data in lst_new_pr:
                    w.writerow({'Код': data[0],
                                'Название': data[1],
                                'Размер': data[2],
                                'Цвет': data[3],
                                'Цена евро': data[4],
                                'Цена грн': data[5],
                                'Наличие': data[6],
                                'Изменения': 'Новые товары'})
            if len(lst_deleted_pr) > 0:
                w.writeheader()
                for data in lst_deleted_pr:
                    w.writerow({'Код': data[0],
                                'Название': data[1],
                                'Размер': data[2],
                                'Цвет': data[3],
                                'Цена евро': data[4],
                                'Цена грн': data[5],
                                'Наличие': data[6],
                                'Изменения': 'Удаленные'})



        return f'Файл {monitoring_file} создан в {path}'
    else:
        return f'Изменений не найдено'

