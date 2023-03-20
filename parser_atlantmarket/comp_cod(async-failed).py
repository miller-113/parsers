import csv
import datetime
from threading import Thread
import datetime
import time


def read_csv(file_name):
    result = []
    with open(f'{file_name}', encoding='utf8') as f1:
        reader = csv.reader(f1)
        for row in reader:
            result.append(row)
    return result


def compare_data(old_file, new_file, p=None):
    old = read_csv(old_file)
    new = read_csv(new_file)
    pools = 36
    if p == 1:
        old = old[:len(old) // pools]
        new = new[:len(old) // pools]
    if p == 2:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 3:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 4:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 5:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 6:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 7:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 8:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 9:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 10:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 11:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 12:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 13:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 14:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 15:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 16:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 17:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 18:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 19:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 20:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 21:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 22:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 23:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 24:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 25:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 26:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 27:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 28:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 29:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 30:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 31:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 32:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 33:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 34:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 35:
        old = old[len(old) * (p - 1) // pools:len(old) * p // pools]
        new = new[len(old) * (p - 1) // pools:len(old) * p // pools]
    if p == 36:
        old = old[len(old) * (p - 1) // pools:]
        new = new[len(old) * (p - 1) // pools:]

    lst_new_pr = []
    lst_modified_pr = []
    lst_deleted_pr = []
    temp = set()
    temp1 = set()
    new_: str
    old_: str

    repl = lambda x: x.replace('>', '').strip()
    # for old_ in tqdm(old[:500]):
    for old_ in old[:100]:
        for new_ in new[:100]:
            count = 0

            if new_ not in old:
                if new_[0] == old_[0]:
                    if new_[6] != old_[6] or new_[7] != old_[7] or str(repl(new_[5])) == '0' and str(
                            repl(old_[5])) != '0' or str(repl(new_[5])) != '0' and str(repl(old_[5])) == '0':
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
    return [lst_modified_pr, lst_new_pr, lst_deleted_pr]


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def checker_for_new_n_modified(monitoring_file, path, old_file, new_file):
    start_time = datetime.datetime.now()
    print(f'Старт {start_time}')
    lst_new_pr = []
    lst_modified_pr = []
    lst_deleted_pr = []
    t1 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 1))
    t2 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 2))
    t3 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 3))
    t4 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 4))
    t5 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 5))
    t6 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 6))
    t7 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 7))
    t8 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 8))
    t9 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 9))
    t10 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 10))
    t11 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 11))
    t12 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 12))
    t13 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 13))
    t14 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 14))
    t15 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 15))
    t16 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 16))
    t17 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 17))
    t18 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 18))
    t19 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 19))
    t20 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 20))
    t21 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 21))
    t22 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 22))
    t23 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 23))
    t24 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 24))
    t25 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 25))
    t26 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 26))
    t27 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 27))
    t28 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 28))
    t29 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 29))
    t30 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 30))
    t31 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 31))
    t32 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 32))
    t33 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 33))
    t34 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 34))
    t35 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 35))
    t36 = ThreadWithReturnValue(target=compare_data, args=(old_file, new_file, 36))
    tasks = []
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()
    t17.start()
    t18.start()
    t19.start()
    t20.start()
    t21.start()
    t22.start()
    t23.start()
    t24.start()
    t25.start()
    t26.start()
    t27.start()
    t28.start()
    t29.start()
    t30.start()
    t31.start()
    t32.start()
    t33.start()
    t34.start()
    t35.start()
    t36.start()
    # tasks = [i for i in range(1, 37)]
    # [i.start() for i in tasks]

    # lst = [{
    # 'modif': [t1.join()[0], t2.join()[0], t3.join()[0], t4.join()[0], t5.join()[0], t6.join()[0], t7.join()[0], t8.join()[0], t9.join()[0], t10.join()[0], t11.join()[0], t12.join()[0],
    #                     t13.join()[0], t14.join()[0], t15.join()[0], t16.join()[0], t17.join()[0], t18.join()[0], t19.join()[0], t20.join()[0], t21.join()[0], t22.join()[0], t23.join()[0], t24.join()[0],
    #                     t25.join()[0], t26.join()[0], t27.join()[0], t28.join()[0], t29.join()[0], t30.join()[0], t31.join()[0], t32.join()[0], t33.join()[0], t34.join()[0], t35.join()[0], t36.join()[0],],

    # 'new':[t1.join()[1], t2.join()[1], t3.join()[1], t4.join()[1], t5.join()[1], t6.join()[1], t7.join()[1], t8.join()[1], t9.join()[1], t10.join()[1], t11.join()[1], t12.join()[1],
    #                     t13.join()[1], t14.join()[1], t15.join()[1], t16.join()[1], t17.join()[1], t18.join()[1], t19.join()[1], t20.join()[1], t21.join()[1], t22.join()[1], t23.join()[1], t24.join()[1],
    #                     t25.join()[1], t26.join()[1], t27.join()[1], t28.join()[1], t29.join()[1], t30.join()[1], t31.join()[1], t32.join()[1], t33.join()[1], t34.join()[1], t35.join()[1], ],

    # 'del':[t1.join()[2], t2.join()[2], t3.join()[2], t4.join()[2], t5.join()[2], t6.join()[2], t7.join()[2], t8.join()[2], t9.join()[2], t10.join()[2], t11.join()[2], t12.join()[2],
    #                     t13.join()[2], t14.join()[2], t15.join()[2], t16.join()[2], t17.join()[2], t18.join()[2], t19.join()[2], t20.join()[2], t21.join()[2], t22.join()[2], t23.join()[2], t24.join()[2],
    #                     t25.join()[2], t26.join()[2], t27.join()[2], t28.join()[2], t29.join()[2], t30.join()[2], t31.join()[2], t32.join()[2], t33.join()[2], t34.join()[2], t35.join()[2], t36.join()[2],]
    # }]
    print()
    for i in enumerate(t1.join()):
        print(i[0], len(i[1]), i[1])
    # lst_modified_pr = lst[0].get('modif')[0]
    # lst_new_pr = lst[0].get('new')[0]
    # lst_deleted_pr = lst[0].get('del')[0]
    # for i in lst_new_pr:
    #     print(i)
    # lst_modified_pr.append([t1.join()[0], t2.join()[0], t3.join()[0], t4.join()[0], t5.join()[0], t6.join()[0], t7.join()[0], t8.join()[0], t9.join()[0], t10.join()[0], t11.join()[0], t12.join()[0],
    #                         t13.join()[0], t14.join()[0], t15.join()[0], t16.join()[0], t17.join()[0], t18.join()[0], t19.join()[0], t20.join()[0], t21.join()[0], t22.join()[0], t23.join()[0], t24.join()[0],
    #                         t25.join()[0], t26.join()[0], t27.join()[0], t28.join()[0], t29.join()[0], t30.join()[0], t31.join()[0], t32.join()[0], t33.join()[0], t34.join()[0], t35.join()[0], t36.join()[0],])
    # lst_modified_pr = lst_modified_pr[0]
    # lst_new_pr.append([t1.join()[1], t2.join()[1], t3.join()[1], t4.join()[1], t5.join()[1], t6.join()[1], t7.join()[1], t8.join()[1], t9.join()[1], t10.join()[1], t11.join()[1], t12.join()[1],
    #                         t13.join()[1], t14.join()[1], t15.join()[1], t16.join()[1], t17.join()[1], t18.join()[1], t19.join()[1], t20.join()[1], t21.join()[1], t22.join()[1], t23.join()[1], t24.join()[1],
    #                         t25.join()[1], t26.join()[1], t27.join()[1], t28.join()[1], t29.join()[1], t30.join()[1], t31.join()[1], t32.join()[1], t33.join()[1], t34.join()[1], t35.join()[1], t36.join()[1],])
    # lst_new_pr = lst_new_pr[0]
    # lst_deleted_pr.append([t1.join()[2], t2.join()[2], t3.join()[2], t4.join()[2], t5.join()[2], t6.join()[2], t7.join()[2], t8.join()[2], t9.join()[2], t10.join()[2], t11.join()[2], t12.join()[2],
    #                         t13.join()[2], t14.join()[2], t15.join()[2], t16.join()[2], t17.join()[2], t18.join()[2], t19.join()[2], t20.join()[2], t21.join()[2], t22.join()[2], t23.join()[2], t24.join()[2],
    #                         t25.join()[2], t26.join()[2], t27.join()[2], t28.join()[2], t29.join()[2], t30.join()[2], t31.join()[2], t32.join()[2], t33.join()[2], t34.join()[2], t35.join()[2], t36.join()[2],])
    # lst_deleted_pr = lst_deleted_pr[0]
    # print('lstmodif' ,lst_modified_pr)
    # print('lstnew' ,lst_new_pr)
    # print('lstdel' ,lst_deleted_pr)

    if len(lst_new_pr) > 0 or len(lst_modified_pr) > 0 or len(lst_deleted_pr) > 0:
        with open(f'{path}{monitoring_file}.csv', 'w', encoding='utf8', newline='') as file:
            fieldnames = ['Код', 'Артикул', 'Статус', 'Найменовання', 'Сертифiкат', 'Залишок', 'Опт', 'РРЦ',
                          'Изменения']

            w = csv.DictWriter(file, fieldnames=fieldnames)

            if len(lst_modified_pr) > 0:
                w.writeheader()
                for fields in range(len(lst_modified_pr[0])):
                    ch = 0
                    str_attr = ''
                    ch += 1
                    if str(lst_modified_pr[0][fields].get('OLD')[6]) != str(
                            lst_modified_pr[0][fields].get('NEW')[6]) and \
                            ch == 1:
                        str_attr += 'Опт'
                    if str(lst_modified_pr[0][fields].get('OLD')[7]) != str(
                            lst_modified_pr[0][fields].get('NEW')[7]) and \
                            ch == 1:
                        str_attr += 'РРЦ'
                    if str(lst_modified_pr[0][fields].get('OLD')[5]) != str(
                            lst_modified_pr[0][fields].get('NEW')[5]) and \
                            ch == 1:
                        str_attr += 'Залишок'
                    w.writerow({
                        'Код': lst_modified_pr[0][fields].get('NEW')[0],
                        'Артикул': lst_modified_pr[0][fields].get('NEW')[1],
                        'Статус': lst_modified_pr[0][fields].get('NEW')[2],
                        'Найменовання': lst_modified_pr[0][fields].get('NEW')[3],
                        'Сертифiкат': lst_modified_pr[0][fields].get('NEW')[4],
                        'Залишок': lst_modified_pr[0][fields].get('NEW')[5],
                        'Опт': lst_modified_pr[0][fields].get('NEW')[6],
                        'РРЦ': lst_modified_pr[0][fields].get('NEW')[7],
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
        print(f"Время работы программы :{datetime.datetime.now() - start_time}")
        return f'Файл {monitoring_file} создан в {path}'
    else:
        print(f"Время работы программы :{datetime.datetime.now() - start_time}")
        return f'Изменений не найдено'


if __name__ == '__main__':
    checker_for_new_n_modified('testdata3.csv', 'testdata3 — копия.csv')
