import csv
import datetime
import itertools
import os
from tqdm import tqdm

FILE_PATH_MONITORING = r'C:\Users\mille\Desktop\HW\\'


# FILE_PATH_MONITORING = r'\\192.168.1.11\Volume_1\Price\\'


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

            if new_[1] + new_[5] == old_[1] + old_[5]:
                if new_[2] != old_[2] or new_[3] != old_[3] or new_[5] != \
                        old_[5]:
                    # or str(new_[3]) \
                    # == '0' and str(old_[3]) != '0' or str(
                    # new_[3]) != '0' and str(old_[3]) == '0':
                    lst_modified_pr.append({
                        'OLD': old_, 'NEW': new_
                    })
            temp1.add(old_[1] + old_[5])
            temp.add(new_[1] + new_[5])

    lst_modified_pr, lst_modified_pr = \
        sorted(lst_modified_pr, key=lambda x: x.get('NEW')[0]), \
        sorted(lst_modified_pr, key=lambda x: x.get('OLD')[0])

    attr_id_prod = temp - temp1
    attr_id_prod1 = temp1 - temp

    for products in new:
        for id_prod in attr_id_prod:
            if id_prod == products[1] + products[5]:
                lst_new_pr.append(products)
    lst_new_pr = sorted(lst_new_pr, key=lambda x: x[0])

    for products in old:
        for id_prod in attr_id_prod1:
            if id_prod == products[1] + products[5]:
                lst_deleted_pr.append(products)
    lst_deleted_pr = sorted(lst_deleted_pr, key=lambda x: x[0])

    if len(lst_new_pr) > 0 or len(lst_modified_pr) > 0 or len(
            lst_deleted_pr) > 0:
        with open(f'{path}{monitoring_file}.csv', 'w', encoding='utf8',
                  newline='') as file:
            fieldnames = ['Название', 'Артикул', 'Цена',
                          'Старая цена', 'Ссылка', 'Размер', 'Изменения']
            w = csv.DictWriter(file, fieldnames=fieldnames)

            if len(lst_modified_pr) > 0:
                w.writeheader()
                for fields in range(len(lst_modified_pr)):
                    ch = 0
                    str_attr = ''
                    ch += 1
                    if str(lst_modified_pr[fields].get('OLD')[5]) != str(
                            lst_modified_pr[fields].get('NEW')[5]) and \
                            ch == 1:
                        str_attr += 'Размер'
                    if str(lst_modified_pr[fields].get('OLD')[2]) != str(
                            lst_modified_pr[fields].get('NEW')[2]) and \
                            ch == 1:
                        str_attr += 'Цена'
                    if str(lst_modified_pr[fields].get('OLD')[3]) != str(
                            lst_modified_pr[fields].get('NEW')[3]) and \
                            ch == 1:
                        str_attr += 'Старая цена'
                    w.writerow({
                        'Название': lst_modified_pr[fields].get('NEW')[0],
                        'Артикул': lst_modified_pr[fields].get('NEW')[1],
                        'Цена': lst_modified_pr[fields].get('NEW')[2],
                        'Старая цена': lst_modified_pr[fields].get('NEW')[3],
                        'Ссылка': lst_modified_pr[fields].get('NEW')[4],
                        'Размер': lst_modified_pr[fields].get('NEW')[5],
                        'Изменения': str_attr,
                    }
                    )

            if len(lst_new_pr) > 0:
                w.writeheader()
                for data in lst_new_pr:
                    w.writerow({
                        'Название': data[0],
                        'Артикул': data[1],
                        'Цена': data[2],
                        'Старая цена': data[3],
                        'Ссылка': data[4],
                        'Размер': data[5],
                        'Изменения': 'Новые товары'})
            if len(lst_deleted_pr) > 0:
                w.writeheader()
                for data in lst_deleted_pr:
                    w.writerow({
                        'Название': data[0],
                        'Артикул': data[1],
                        'Цена': data[2],
                        'Старая цена': data[3],
                        'Ссылка': data[4],
                        'Размер': data[5],
                        'Изменения': 'Удаленные'})

        return f'Файл {monitoring_file} создан в {path}'
    else:
        return f'Изменений не найдено'


if __name__ == '__main__':
    print(checker_for_new_n_modified(
        r"C:\Users\mille\Desktop\HW\totalfit_first.csv",
        r"C:\Users\mille\Desktop\HW\totalfit_second.csv",
        'monitoring_data',
        r"C:\Users\mille\Desktop\HW\\"))
