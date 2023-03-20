import csv
import re

from main import *
from tqdm import tqdm


def nan(lst):
    mod_lst = []
    for i in range(len(lst)):
        # if i == 0:
        #     continue
        if type(lst[i]) == datetime.datetime:
            lst[i] = ''
        if type(lst[i]) != str:
            if numpy.isnan(lst[i]):
                lst[i] = ''
            elif not numpy.isnan(lst[i]):
                lst[i] = lst[i]
        mod_lst.append(lst[i])
    return mod_lst


def read_csv(file):
    result = []
    reader = pd.read_csv(file)
    for row in reader.values.tolist():
        result.append(nan(row))
    return result

def checker_for_new_n_modified(old_file, new_file):
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
            # if new_ not in old:
                # if new_[1] == '' or old_[1] == '':
                #     continue

            if new_[-3] == old_[-3]:
                if new_[-2] != old_[-2] or new_[-1] != old_[-1]:
                    lst_modified_pr.append({
                        'OLD': old_, 'NEW': new_
                    })

            temp1.add(old_[-3])
            temp.add(new_[-3])

    attr_id_prod = temp - temp1
    attr_id_prod1 = temp1 - temp
    for products in new:
        for id_prod in attr_id_prod:
            if id_prod == products[-3]:
                lst_new_pr.append(products)

    for products in old:
        for id_prod in attr_id_prod1:
            if id_prod == products[-3]:
                lst_deleted_pr.append(products)
    return [lst_modified_pr, lst_new_pr, lst_deleted_pr]


def csv_writer(old_f, new_f, file_path_to_save, file_name):
    comp_funk = checker_for_new_n_modified(old_f, new_f)
    lst_modified_pr = comp_funk[0]
    lst_new_pr = comp_funk[1]
    lst_deleted_pr = comp_funk[2]
    time_d_m = datetime.datetime.now().strftime('%d.%m')
    if len(lst_modified_pr) > 0 or len(lst_new_pr) > 0 or len(lst_deleted_pr) > 0:

        with open(f'{file_path_to_save}{file_name}{time_d_m}.csv', 'w', encoding='utf8', newline='') as file:
            fieldnames = ['Артикул', 'Объем.мл', 'Наименование(укр)', 'Цвет(укр)', 'Габариты(В * Д)', 'Вес.грамм',
                          'Артикул.1', 'РРЦ.грн', 'Наличие', 'Изменения']
            w = csv.DictWriter(file, fieldnames=fieldnames)
            if len(lst_modified_pr) > 0:
                w.writeheader()
                for dt in lst_modified_pr:
                    changes = ''

                    if dt.get('OLD')[-2] != dt.get('NEW')[-2]:
                            changes += f'Цена'
                    if dt.get('OLD')[-1] != dt.get('NEW')[-1]:
                            changes += f'Наличие'

                    w.writerow({
                        'Артикул': re.findall('\d{4}', dt.get('NEW')[5])[0],
                        'Объем.мл': re.findall('\d{2,5} мл', dt.get('NEW')[5])[0],
                        'Наименование(укр)': re.sub('\d{4}|\d{2,5} мл', '', dt.get('NEW')[5]),
                        'Цвет(укр)': dt.get('NEW')[6],
                        'Габариты(В * Д)': dt.get('NEW')[7],
                        'Вес.грамм': dt.get('NEW')[8],
                        'Артикул.1': dt.get('NEW')[9],
                        'РРЦ.грн': f"{dt.get('NEW')[10]:.0f}",
                        'Наличие': dt.get('NEW')[11],
                        'Изменения': changes,
                    })
            if len(lst_new_pr) > 0:
                w.writeheader()
                for dt in lst_new_pr:
                    w.writerow({
                        'Артикул': re.findall('\d{4}', dt[5])[0],
                        'Объем.мл': re.findall('\d{2,5} мл', dt[5])[0],
                        'Наименование(укр)': re.sub('\d{4}|\d{2,5} мл', '', dt[5]),
                        'Цвет(укр)': dt[6],
                        'Габариты(В * Д)': dt[7],
                        'Вес.грамм': dt[8],
                        'Артикул.1': dt[9],
                        'РРЦ.грн': f"{dt[10]:.0f}",
                        'Наличие': dt[11],
                        'Изменения': 'Новые товары',
                    })
            if len(lst_deleted_pr) > 0:
                w.writeheader()
                for dt in lst_deleted_pr:
                    w.writerow({
                        'Артикул': re.findall('\d{4}', dt[5])[0],
                        'Объем.мл': re.findall('\d{2,5} мл', dt[5])[0],
                        'Наименование(укр)': re.sub('\d{4}|\d{2,5} мл', '', dt[5]),
                        'Цвет(укр)': dt[6],
                        'Габариты(В * Д)': dt[7],
                        'Вес.грамм': dt[8],
                        'Артикул.1': dt[9],
                        'РРЦ.грн': f"{dt[10]:.0f}",
                        'Наличие': dt[11],
                        'Изменения': 'Удаленные товары',
                    })
        return f'Файл создан'
    else:
        return f'Изменений не найдено'
