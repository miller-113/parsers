import csv
import datetime
import itertools
import os
# from auth import *
from tqdm import tqdm


def read_csv(file_name):
    result = []
    with open(f'{file_name}', encoding='utf8') as f1:
        reader = csv.reader(f1)
        for row in reader:
            result.append(row)
    return result


def checker_for_new_n_modified(old_file, new_file,
                               monitoring_file='monitoringdata', path=None):
    old = read_csv(old_file)
    new = read_csv(new_file)
    lst_new_pr = []
    lst_modified_pr = []
    lst_deleted_pr = []
    temp = set()
    temp1 = set()
    new_: str
    old_: str
    repl = lambda x: x.replace('>', '').strip()
    for old_ in tqdm(old):
        for new_ in new:
            if new_[0] == old_[0]:
                if new_[6] != old_[6] or new_[7] != old_[7] or str(
                        repl(new_[5])) == '0' and str(
                        repl(old_[5])) != '0' or str(
                        repl(new_[5])) != '0' and str(repl(old_[5])) == '0':
                    lst_modified_pr.append({
                        'OLD': old_, 'NEW': new_
                    })

            temp1.add(old_[0])
            temp.add(new_[0])

    attr_id_prod = temp - temp1
    attr_id_prod1 = temp1 - temp
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
            fieldnames = ['Код', 'Артикул', 'Статус', 'Найменовання',
                          'Сертифiкат', 'Залишок', 'Опт', 'РРЦ', 'Изменения']

            w = csv.DictWriter(file, fieldnames=fieldnames)

            if len(lst_modified_pr) > 0:
                w.writeheader()
                for fields in range(len(lst_modified_pr)):
                    ch = 0
                    str_attr = ''
                    ch += 1
                    if str(lst_modified_pr[fields].get('OLD')[6]) != str(
                            lst_modified_pr[fields].get('NEW')[6]) and \
                            ch == 1:
                        str_attr += 'Опт'
                    if str(lst_modified_pr[fields].get('OLD')[7]) != str(
                            lst_modified_pr[fields].get('NEW')[7]) and \
                            ch == 1:
                        str_attr += 'РРЦ'
                    if str(lst_modified_pr[fields].get('OLD')[5]) != str(
                            lst_modified_pr[fields].get('NEW')[5]) and \
                            ch == 1:
                        str_attr += 'Залишок'
                    w.writerow({
                        'Код': lst_modified_pr[fields].get('NEW')[0],
                        'Артикул': lst_modified_pr[fields].get('NEW')[1],
                        'Статус': lst_modified_pr[fields].get('NEW')[2],
                        'Найменовання': lst_modified_pr[fields].get('NEW')[3],
                        'Сертифiкат': lst_modified_pr[fields].get('NEW')[4],
                        'Залишок': lst_modified_pr[fields].get('NEW')[5],
                        'Опт': lst_modified_pr[fields].get('NEW')[6],
                        'РРЦ': lst_modified_pr[fields].get('NEW')[7],
                        'Изменения': str_attr,
                    }
                    )

            if len(lst_new_pr) > 0:
                w.writeheader()
                for data in lst_new_pr:
                    w.writerow({
                        'Код': data[0],
                        'Артикул': data[1],
                        'Статус': data[2],
                        'Найменовання': data[3],
                        'Сертифiкат': data[4],
                        'Залишок': data[5],
                        'Опт': data[6],
                        'РРЦ': data[7],
                        'Изменения': 'Новые товары'})
            if len(lst_deleted_pr) > 0:
                w.writeheader()
                for data in lst_deleted_pr:
                    w.writerow({
                        'Код': data[0],
                        'Артикул': data[1],
                        'Статус': data[2],
                        'Найменовання': data[3],
                        'Сертифiкат': data[4],
                        'Залишок': data[5],
                        'Опт': data[6],
                        'РРЦ': data[7],
                        'Изменения': 'Удаленные'})

        return f'Файл {monitoring_file} создан в {path}'
    else:
        return f'Изменений не найдено'
