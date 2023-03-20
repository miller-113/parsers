import csv
import random
import time
from text_to_code import get_cod_from_str
from bs4 import BeautifulSoup
from CONST import *


def get_categories_urls():
    req = session.get(url_catalog, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')

    categories_links = soup.find('div',
                                 class_='catalog-tovars__podbor__cover').find_all(
        'a')
    categories_links_lst = [cat_lin.get('href') for cat_lin in categories_links]
    return categories_links_lst


def get_product_urls(cat_links=None):
    global pr_url

    if cat_links is None:
        cat_links = get_categories_urls()
    else:
        cat_links = cat_links.split()

    temp_for_links = []
    try:
        for pr_url in cat_links:
            req = session.get(pr_url, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')

            if soup.find('div',
                         class_='tovarlist tovarlist-centerWhenOne') is not None:
                pr_links_on_page = soup.find('div',
                                             class_='tovarlist tovarlist-centerWhenOne'). \
                    find_all('div', class_='tovarsmall__cover')
                # получаем ссылки на продукты из категорий и фильтруем на одинаковые ссылки
                for i in pr_links_on_page:
                    if i.find('div', class_='tovarsmall__topcover').find(
                            'a').get('href') not in temp_for_links:
                        temp_for_links.append(
                            i.find('div', class_='tovarsmall__topcover').find(
                                'a').get('href'))
                    else:
                        continue
            time.sleep(random.randint(2, 4))
    except Exception as e:
        print(e, pr_url)
    return temp_for_links


def get_products_data(choice=None):
    if choice == 'manual':
        urls = get_product_urls(input('Введите ссылки категорий через пробел'))
    else:
        urls = get_product_urls()

    urls_count = len(urls)
    product_data = []
    for pr_link in enumerate(urls):
        req = session.get(pr_link[1], headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')

        size_of_pr = soup.find_all('div', class_='one-tovar__sizes__size__info')
        counter = 1
        # try:
        for i in range(len(size_of_pr)):
            if size_of_pr[i].find_parent().find('select') is None:
                name = f"{str(counter)} {soup.find('div', class_='one-tovar__name').text.strip()}"
                vkus = ''
                size = size_of_pr[i].find_parent().find('div',
                                                        class_='one-tovar__sizes__size__info__ves').text.strip()
                cena = size_of_pr[i].find_parent().find('div',
                                                        class_='one-tovar__sizes__size__price').text.strip()
                cena_old_n_new = cena.translate(
                    {ord(i): None for i in (' ', '\n')}).split('грн')
                pr_id = soup.find_all('div', class_='one-tovar__sizes__size')[
                    i].get('data-tovar-anons')
                lamda = lambda x: x.get('alt') if x is not None else 'В наличии'
                if soup.find('div',
                             class_='one-tovar__sizes__size__info') is not None:
                    in_stock = lamda(size_of_pr[i].find_parent().find('div',
                                                                      class_='tovar__plashka').find(
                        'img'))
                    if 'red' in in_stock or 'красный' in in_stock:
                        in_stock = 'В наличии'
                else:
                    in_stock = 'В наличии'

                product_data.append({
                    'Name': name,
                    'Url': pr_link[1],
                    'Vkus': vkus,
                    'In stock': in_stock,
                    'Size': size,
                    'New price': cena_old_n_new[1] if cena_old_n_new[
                                                          1] != '' else
                    cena_old_n_new[0],
                    'Old price': '' if cena_old_n_new[1] == '' else
                    cena_old_n_new[0],
                    'Id': pr_id,
                })
            else:
                for l in enumerate(
                        size_of_pr[i].find_parent().find('select').find_all(
                                'option')):
                    name = f"{str(counter)} {soup.find('div', class_='one-tovar__name').text.strip()}"
                    vkus = l[1].text.strip()
                    vkus_id = l[1].get('value')
                    vkus_id_tabl = l[1].find_parent().get('data-size-vkus')
                    lam = lambda x: x.get(
                        'alt') if x is not None else 'В наличии'
                    if soup.find('div',
                                 class_='one-tovar__sizes__size__info') is not None:
                        in_stock = lam(size_of_pr[i].find_parent().find('div',
                                                                        class_='tovar__plashka').find(
                            'img'))
                        if 'red' in in_stock or 'красный' in in_stock:
                            in_stock = 'В наличии'
                    else:
                        in_stock = 'В наличии'

                    size = size_of_pr[i].find_parent().find('div',
                                                            class_='one-tovar__sizes__size__info__ves'). \
                        text.strip()
                    cena = size_of_pr[i].find_parent().find('div',
                                                            class_='one-tovar__sizes__size__price').text.strip()
                    pr_id = \
                    soup.find_all('div', class_='one-tovar__sizes__size')[
                        i].get('data-tovar-anons')

                    cena_old_n_new = cena.translate(
                        {ord(i): None for i in (' ', '\n')}).split('грн')
                    product_data.append({
                        'Name': name,
                        'Url': pr_link[1],
                        'Vkus': vkus,
                        'In stock': in_stock,
                        'Size': size,
                        'New price': cena_old_n_new[1] if cena_old_n_new[
                                                              1] != '' else
                        cena_old_n_new[0],
                        'Old price': '' if cena_old_n_new[1] == '' else
                        cena_old_n_new[0],
                        'Id': pr_id + vkus_id_tabl + vkus_id,
                    })
                    counter += 1
            time.sleep(random.randint(2, 4))
        print(f'Отработала {pr_link[1]} {pr_link[0] + 1} c {urls_count}')
        # except Exception as e:
        #     print(e, pr_link)
        #     continue
    return product_data


def csv_writer(path=FILE_PATH_PARS, file_name='testdata', mode='1'):
    global pr_data
    if mode == '1':
        pr_data = get_products_data('manual')
    elif mode == '2':
        pr_data = get_products_data()
    with open(f'{path}{file_name}.csv', mode='w', newline='',
              encoding='utf8') as product_date:
        fieldnames = ['Название', 'Ссылка', 'Цена', 'Старая цена', 'Наличие',
                      'Вкус/Цвет', 'Ид', 'Размер', 'TY']
        product_date_writer = csv.DictWriter(product_date,
                                             fieldnames=fieldnames)
        product_date_writer.writeheader()

        for pr in pr_data:
            product_date_writer.writerow(
                {'Название': pr.get('Name'), 'Ссылка': pr.get('Url'),
                 'Цена': pr.get('New price'),
                 'Старая цена': pr.get('Old price'),
                 'Наличие': pr.get('In stock'), 'Вкус/Цвет': pr.get('Vkus'),
                 'Ид': pr.get('Id'), 'Размер': pr.get('Size')})

    return f'Создан {file_name} в {path}'
