import csv
import datetime
import itertools
import os
# from CONST import *
import sqlite3
from main import FILE_PATH_PARS, FILE_PATH_MONITORING


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
        if new_[6] == old_[6]:
            lst_modified_pr.append({
                'OLD': old_, 'NEW': new_
            })
        temp1.add(old_[6])
        temp.add(new_[6])

    attr_id_prod = temp - temp1
    attr_id_prod1 = temp1 - temp
    # ищем новые товары
    for products in new:
        for id_prod in attr_id_prod:
            if id_prod == products[6]:
                lst_new_pr.append(products)

    for products in old:
        for id_prod in attr_id_prod1:
            if id_prod == products[6]:
                lst_deleted_pr.append(products)

    if len(lst_new_pr) > 0 or len(lst_modified_pr) > 0 or len(
            lst_deleted_pr) > 0:
        with open(f'{path}{monitoring_file}.csv', 'w', encoding='utf8',
                  newline='') as file:
            fieldnames = ['Название', 'Ссылка', 'Цена', 'Старая цена',
                          'Наличие', 'Вкус/Цвет', 'Ид', 'Размер',
                          'Изменения']
            w = csv.DictWriter(file, fieldnames=fieldnames)
            # date_time = datetime.datetime.now().strftime('%d.%m %H:%M')

            # a = sqlite3.connect(f'{path}db_monitoring.db')
            # cur = a.cursor()
            # cur.execute('''CREATE TABLE IF NOT EXISTS 'products'(
            #         current_date text, pr_id text, pr_name text, pr_size text, pr_color text, pr_price_euro text,
            #         pr_price_ua text, pr_in_stock text, changes text) ''')
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
                    if str(lst_modified_pr[fields].get('OLD')[1]) != str(
                            lst_modified_pr[fields].get('NEW')[1]) and \
                            ch == 1:
                        str_attr += 'Ссылка'
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
                        str_attr += 'Наличие'
                    if str(lst_modified_pr[fields].get('OLD')[5]) != str(
                            lst_modified_pr[fields].get('NEW')[5]) and \
                            ch == 1:
                        str_attr += 'Вкус/Цвет'
                    if str(lst_modified_pr[fields].get('OLD')[6]) != str(
                            lst_modified_pr[fields].get('NEW')[6]) and \
                            ch == 1:
                        str_attr += 'Ид'
                    if str(lst_modified_pr[fields].get('OLD')[7]) != str(
                            lst_modified_pr[fields].get('NEW')[7]) and \
                            ch == 1:
                        str_attr += 'Размер'
                    w.writerow(
                        {'Название': lst_modified_pr[fields].get('NEW')[0],
                         'Ссылка': lst_modified_pr[fields].get('NEW')[1],
                         'Цена': lst_modified_pr[fields].get('NEW')[2],
                         'Старая цена': lst_modified_pr[fields].get('NEW')[3],
                         'Наличие': lst_modified_pr[fields].get('NEW')[4],
                         'Вкус/Цвет': lst_modified_pr[fields].get('NEW')[5],
                         'Ид': lst_modified_pr[fields].get('NEW')[6],
                         'Размер': lst_modified_pr[fields].get('NEW')[7],
                         'Изменения': str_attr,
                         }
                        )
            # cur.execute('''INSERT INTO products(
            #                 current_date, pr_id, pr_name, pr_size, pr_color, pr_price_euro,
            #                 pr_price_ua, pr_in_stock, changes)VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            #             (str(date_time), str(lst_modified_pr[fields].get('NEW')[0]), str(lst_modified_pr[fields].get('NEW')[1]),
            #              str(lst_modified_pr[fields].get('NEW')[2]), str(lst_modified_pr[fields].get('NEW')[3]),
            #              str(lst_modified_pr[fields].get('NEW')[4]), str(lst_modified_pr[fields].get('NEW')[5]),
            #              str(lst_modified_pr[fields].get('NEW')[6]), str_attr))
            if len(lst_new_pr) > 0:
                w.writeheader()
                for data in lst_new_pr:
                    w.writerow({'Название': data[0],
                                'Ссылка': data[1],
                                'Цена': data[2],
                                'Старая цена': data[3],
                                'Наличие': data[4],
                                'Вкус/Цвет': data[5],
                                'Ид': data[6],
                                'Размер': data[7],
                                'Изменения': 'Новые товары'})
            if len(lst_deleted_pr) > 0:
                w.writeheader()
                for data in lst_deleted_pr:
                    w.writerow({'Название': data[0],
                                'Ссылка': data[1],
                                'Цена': data[2],
                                'Старая цена': data[3],
                                'Наличие': data[4],
                                'Вкус/Цвет': data[5],
                                'Ид': data[6],
                                'Размер': data[7],
                                'Изменения': 'Удаленные'})

                # cur.execute('''INSERT INTO products(
                #                             current_date, pr_id, pr_name, pr_size, pr_color, pr_price_euro,
                #                             pr_price_ua, pr_in_stock, changes)VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                #             (str(date_time), data[0], data[1], data[2], data[3], data[4], data[5], data[6], 'Новые товары'))
        # a.commit()
        # cur.close()
        # a.close()

        return f'Файл {monitoring_file} создан в {path}'
    else:
        return f'Изменений не найдено'

# if __name__ == '__main__':

#     checker_for_new_n_modified('testfile.csv', 'testfile1.csv')
