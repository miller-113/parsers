import csv
import datetime
import itertools
import os

import numpy
import pandas
# from auth import *
from tqdm import tqdm


def find_headers(lst):
    # temp = None
    # for i in enumerate(lst):
    #     # for str_ in i[1]:
    #     if str_ == 'Номенклатура' or str_ == 'Артикул' or \
    #             str_ == 'РРЦ, ₴ грн':
    #         temp = i[0]
    #         break
    lst = (lst[0].split(';')
           if (len(lst) != 0) else ''
           )
    try:
        articul = lst.index('Артикул')
    except ValueError as e:
        articul = 0
        print('Артикул нет в списке поставлен индекс по умолчанию 1')
    try:
        name = lst.index('Код')
    except ValueError as e:
        name = 1
        print('Код нет в списке поставлен индекс по умолчанию 0')
    try:
        price = lst.index('Цена')
    except ValueError as e:
        price = 2
        print('Цена нет в списке поставлен индекс по умолчанию 6')
    try:
        product_rest = lst.index('В наличии')
    except ValueError as e:
        product_rest = 4
        print('В наличии нет в списке поставлен индекс по умолчанию 7')
    
    return articul, name, price, product_rest


def nan(lst):
    mod_lst = []
    for i in lst:
        if type(i) == datetime.datetime:
            i = ''
        if type(i) != str:
            if numpy.isnan(i):
                i = ''
            elif not numpy.isnan(i):
                i = i
        mod_lst.append(i)
    return mod_lst


def read_csv(file_name):
    result = []
    header = []
    with open(f'{file_name}', 'rb') as f1:
        reader = pandas.read_csv(f1)
        for row in reader.values.tolist():
            result.append(nan(row))
        header = reader.head(0).columns.values.tolist()
    return result, header


def checker_for_new_n_modified(old_file, new_file,
                               monitoring_file='monitoringdata', path=None):
    old, old_header = read_csv(old_file)
    new, new_header = read_csv(new_file)
    lst_new_pr = []
    lst_modified_pr = []
    lst_deleted_pr = []
    temp = set()
    temp1 = set()
    
    old_art, old_name, old_price, old_rest = find_headers(old_header)
    new_art, new_name, new_price, new_rest = find_headers(new_header)
    
    for old_ in tqdm(old):
        if len(old_) == 0:
            continue
        old_ = old_[0].split(';')
        for new_ in new:
            if len(new_) == 0:
                continue
            new_ = new_[0].split(';')
            if new_[new_art] + new_[new_name] == old_[old_art] + old_[old_name]:
                # if new_[new_rest] != old_[old_rest] or \
                if new_[new_rest] == '0' and old_[old_rest] != '0' or \
                        new_[new_rest] != '0' and old_[old_rest] == '0' or \
                        new_[new_price] != old_[old_price]:
                    lst_modified_pr.append({
                        'OLD': old_, 'NEW': new_
                    })
            
            temp1.add(old_[old_art] + old_[old_name])
            temp.add(new_[new_art] + new_[new_name])
    
    attr_id_prod = temp - temp1
    attr_id_prod1 = temp1 - temp
    for products in new:
        if len(products) == 0:
            continue
        products = products[0].split(';')
        for id_prod in attr_id_prod:
            if id_prod == products[new_art] + products[new_name]:
                lst_new_pr.append(products)
    
    for products in old:
        if len(products) == 0:
            continue
        products = products[0].split(';')
        for id_prod in attr_id_prod1:
            if id_prod == products[old_art] + products[old_name]:
                lst_deleted_pr.append(products)
    
    if len(lst_new_pr) > 0 or len(lst_modified_pr) > 0 or len(
            lst_deleted_pr) > 0:
        with open(f'{path}{monitoring_file}.csv', 'w', encoding='utf8',
                  newline='') as file:
            fieldnames = ['Артикул', 'Код', 'Цена',
                          'В наличии', 'Изменения']
            
            w = csv.DictWriter(file, fieldnames=fieldnames)
            
            if len(lst_modified_pr) > 0:
                w.writeheader()
                for fields in range(len(lst_modified_pr)):
                    ch = 0
                    str_attr = ''
                    ch += 1
                    if str(lst_modified_pr[fields].get('OLD')[old_rest]) != str(
                            lst_modified_pr[fields].get('NEW')[new_rest]) and \
                            ch == 1:
                        str_attr += 'В наличии'
                    if str(lst_modified_pr[fields].get('OLD')[
                               old_price]) != str(
                        lst_modified_pr[fields].get('NEW')[new_price]) and \
                            ch == 1:
                        str_attr += 'Цена'
                    w.writerow({
                        'Артикул': lst_modified_pr[fields].get('NEW')[
                            new_name],
                        'Код': lst_modified_pr[fields].get('NEW')[new_art],
                        'Цена': lst_modified_pr[fields].get('NEW')[
                            new_price],
                        'В наличии': lst_modified_pr[fields].get('NEW')[
                            new_rest],
                        'Изменения': str_attr,
                    }
                    )
            
            if len(lst_new_pr) > 0:
                w.writeheader()
                for data in lst_new_pr:
                    w.writerow({
                        'Артикул': data[new_name],
                        'Код': data[new_art],
                        'Цена': data[new_price],
                        'В наличии': data[new_rest],
                        'Изменения': 'Новые товары'})
            if len(lst_deleted_pr) > 0:
                w.writeheader()
                for data in lst_deleted_pr:
                    w.writerow({
                        'Артикул': data[new_name],
                        'Код': data[new_art],
                        'Цена': data[new_price],
                        'В наличии': data[new_rest],
                        'Изменения': 'Удаленные'})
        
        return f'Файл {monitoring_file} создан в {path}'
    else:
        return f'Изменений не найдено'
