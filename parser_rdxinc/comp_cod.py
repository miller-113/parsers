import csv
import datetime
import itertools
import os
from auth import *
from tqdm import tqdm


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
                if new_[0] != old_[0] or new_[2] != old_[2] or new_[3] != old_[
                    3] or str(new_[4]) == '0' and \
                        str(old_[4]) != '0' or str(new_[4]) != '0' and str(
                    old_[4]) == '0' \
                        or new_[5] != old_[5] or new_[6] != old_[6] or new_[
                    9] != old_[9]:
                    lst_modified_pr.append({
                        'OLD': old_, 'NEW': new_
                    })
            temp1.add(old_[1])
            temp.add(new_[1])

    attr_id_prod = temp - temp1
    attr_id_prod1 = temp1 - temp
    # ищем новые товары
    for products in new:
        for id_prod in attr_id_prod:
            if id_prod == products[1]:
                lst_new_pr.append(products)

    for products in old:
        for id_prod in attr_id_prod1:
            if id_prod == products[1]:
                lst_deleted_pr.append(products)

    if len(lst_new_pr) > 0 or len(lst_modified_pr) > 0 or len(
            lst_deleted_pr) > 0:
        with open(f'{path}{monitoring_file}.csv', 'w', encoding='utf8',
                  newline='') as file:
            fieldnames = ['Название', 'Ссылка', 'Цена', 'Старая цена',
                          'НаличиеКолл.', 'Наличие', 'Бренд', 'Ид',
                          'Доп.Ид', 'Размер', 'Изменения']
            w = csv.DictWriter(file, fieldnames=fieldnames)

            if len(lst_modified_pr) > 0:
                w.writeheader()
                for fields in range(len(lst_modified_pr)):
                    ch = 0
                    str_attr = ''
                    ch += 1
                    if str(lst_modified_pr[fields].get('OLD')[0]) != str(
                            lst_modified_pr[fields].get('NEW')[0]) and \
                            ch == 1:
                        str_attr += 'Название'
                    if str(lst_modified_pr[fields].get('OLD')[2]) != str(
                            lst_modified_pr[fields].get('NEW')[2]) and \
                            ch == 1:
                        str_attr += 'Цена'
                    if str(lst_modified_pr[fields].get('OLD')[3]) != str(
                            lst_modified_pr[fields].get('NEW')[3]) and \
                            ch == 1:
                        str_attr += 'Старая цена'
                    if str(lst_modified_pr[fields].get('OLD')[4]) != str(
                            lst_modified_pr[fields].get('NEW')[4]) and \
                            ch == 1:
                        str_attr += 'НаличиеКолл.'
                    if str(lst_modified_pr[fields].get('OLD')[5]) != str(
                            lst_modified_pr[fields].get('NEW')[5]) and \
                            ch == 1:
                        str_attr += 'Наличие'
                    if str(lst_modified_pr[fields].get('OLD')[6]) != str(
                            lst_modified_pr[fields].get('NEW')[6]) and \
                            ch == 1:
                        str_attr += 'Бренд'
                    if str(lst_modified_pr[fields].get('OLD')[9]) != str(
                            lst_modified_pr[fields].get('NEW')[9]) and \
                            ch == 1:
                        str_attr += 'Размер'
                    w.writerow({
                        'Название': lst_modified_pr[fields].get('NEW')[0],
                        'Ссылка': lst_modified_pr[fields].get('NEW')[1],
                        'Цена': lst_modified_pr[fields].get('NEW')[2],
                        'Старая цена': lst_modified_pr[fields].get('NEW')[3],
                        'НаличиеКолл.': lst_modified_pr[fields].get('NEW')[4],
                        'Наличие': lst_modified_pr[fields].get('NEW')[5],
                        'Бренд': lst_modified_pr[fields].get('NEW')[6],
                        'Ид': lst_modified_pr[fields].get('NEW')[7],
                        'Доп.Ид': lst_modified_pr[fields].get('NEW')[8],
                        'Размер': lst_modified_pr[fields].get('NEW')[9],
                        'Изменения': str_attr,
                    }
                    )

            if len(lst_new_pr) > 0:
                w.writeheader()
                for data in lst_new_pr:
                    w.writerow({
                        'Название': data[0],
                        'Ссылка': data[1],
                        'Цена': data[2],
                        'Старая цена': data[3],
                        'НаличиеКолл.': data[4],
                        'Наличие': data[5],
                        'Бренд': data[6],
                        'Ид': data[7],
                        'Доп.Ид': data[8],
                        'Размер': data[9],
                        'Изменения': 'Новые товары'})
            if len(lst_deleted_pr) > 0:
                w.writeheader()
                for data in lst_deleted_pr:
                    w.writerow({
                        'Название': data[0],
                        'Ссылка': data[1],
                        'Цена': data[2],
                        'Старая цена': data[3],
                        'НаличиеКолл.': data[4],
                        'Наличие': data[5],
                        'Бренд': data[6],
                        'Ид': data[7],
                        'Доп.Ид': data[8],
                        'Размер': data[9],
                        'Изменения': 'Удаленные'})

        return f'Файл {monitoring_file} создан в {path}'
    else:
        return f'Изменений не найдено'


if __name__ == '__main__':
    checker_for_new_n_modified('testdata3.csv', 'testdata3 — копия.csv')
