import asyncio
import csv
import datetime
import re
import aiohttp
import requests
from bs4 import BeautifulSoup
import fake_useragent
import time

user = fake_useragent.UserAgent().random
headers = {'user-agent': user}


def get_nav_urls():
    site_url = 'https://totalfit.com.ua/'
    request = requests.get(site_url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')
    list_urls_in_nav = []
    urls_in_nav = soup.find('nav', attrs={'id': 'main-nav-wrap'}).find_all('ul')
    for i in urls_in_nav:
        for from_nav in i.find_all('a'):
            temp = from_nav.get('href')
            if 'product-category' in temp and temp not in list_urls_in_nav:
                list_urls_in_nav.append(from_nav.get('href'))
    return list_urls_in_nav


# unnecessary = ['https://totalfit.com.ua/product-category/accessories-uk/',
#                'https://totalfit.com.ua/product-category/iceland-uk/',
#                'https://totalfit.com.ua/product-category/cycling-uk/',
#                'https://totalfit.com.ua/product-category/for-children-uk/',
#                'https://totalfit.com.ua/product-category/thermo-uk/',
#                'https://totalfit.com.ua/product-category/swimsuits-uk/',
#                'https://totalfit.com.ua/product-category/casual-uk/',
#                ]

async def get_html(url, session):
    try:
        # async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            return BeautifulSoup(await resp.text(), "html.parser")

    except Exception as e:
        req = requests.get(url, headers=headers)
        return BeautifulSoup(req.text, "html.parser")


async def get_prod_urls(url, session):
    pr_urls = []
    page = 1
    while page:
        # try:
        request = await get_html(url + f'/page/{page}', session)

        # soup = BeautifulSoup(request, 'lxml')
        soup = request
        pr_on_url = soup.find('div', class_='wpf-search-container')
        if pr_on_url is None:
            page = 0
            continue
        else:
            pr_on_url = pr_on_url.find('ul')
        get_prod_urls_in_page = pr_on_url.find_all('li')
        # prod_urls_in_page = [i.find('a').get('href') for i in
        #                      get_prod_urls_in_page]
        prod_urls_in_page = [i.find('a').get('href')
                             for i in get_prod_urls_in_page if
                             'product-category' not in i.find('a').get('href')]
        pr_urls += prod_urls_in_page
        page += 1
    return pr_urls


async def get_pr_data(url, session):
    global pr_size
    time_ = datetime.datetime.now()

    pr_data = []
    request = await get_html(url, session)
    soup = request
    # soup = BeautifulSoup(request, 'lxml')
    if not soup.find('nav'):
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.text, 'html.parser')
    #
    size = s.find_all('tr') if (s := soup.find('table', class_='variations')) \
        else []
    if len(size) >= 2:
        pr_size_top = ['Top:' + i.text for i in size[0].find_all('option') if
                       i.text != 'Виберіть опцію'] if size else False
        pr_size_bottom = ['Bott:' + i.text for i in size[1].find_all('option')
                          if
                          i.text != 'Виберіть опцію'] if size else False
        pr_size_slip = ['Trunk:' + i.text for i in size[2].find_all('option') if
                        i.text != 'Виберіть опцію'] if len(size) > 2 else None

        if len(pr_size_top) > len(pr_size_bottom):
            pr_size = []
            for i in enumerate(pr_size_bottom):
                pr_size += [[pr_size_top[i[0]], pr_size_bottom[i[0]]]]
            pr_size += [[pr_size_top[-1]]]
            if pr_size_slip is not None:
                pr_size[0] += pr_size_slip

        elif len(pr_size_top) < len(pr_size_bottom):
            pr_size = []
            for i in enumerate(pr_size_top):
                pr_size += [[pr_size_top[i[0]], pr_size_bottom[i[0]]]]
            pr_size += [[pr_size_bottom[-1]]]
            if pr_size_slip is not None:
                pr_size[0] += pr_size_slip

        elif len(pr_size_top) == len(pr_size_bottom) and len(pr_size_top) != 0:
            pr_size = []
            for i in enumerate(pr_size_top):
                pr_size += [[pr_size_top[i[0]], pr_size_bottom[i[0]]]]
            if pr_size_slip is not None:
                pr_size[0] += pr_size_slip

    elif len(size) == 1:
        pr_size = [i.text for i in size[0].find_all('option') if
                   i.text != 'Виберіть опцію']
    else:
        pr_size = (['відсутній']
                   if 'відсутній' in request.text
                   else ['']
                   )
    # drop_down = soup.find_all('select')
    # if len(drop_down) == 2:
    #
    #     pr_size = [i.text for i in drop_down[0].find_all('option') if
    #                i.text != 'Виберіть опцію']
    #     if 'Оцінка…' in pr_size:
    #         pr_size = ['Відсутній']
    #
    # elif len(drop_down) >= 3:
    #     get_form = soup.find(attrs={'class': 'variations_form cart'}).get(
    #         'data-product_variations')
    #     pr_size_top = ['Top:' + str(i).upper()
    #                    for i in re.findall(r'"attribute_pa_top-size":"(\w+)',
    #                                        get_form)
    #                    ]
    #
    #     if len(pr_size_top) == 0:
    #         pr_size_top = ['Top:' + i.text for i in drop_down[0].find_all
    #         ('option') if i.text != 'Виберіть опцію']
    #
    #     pr_size_bottom = ['Bottom:' + str(i).upper()
    #                       for i in
    #                       re.findall(r'"attribute_pa_bottom-size":"(\w+)',
    #                                  get_form)
    #                       ]
    #     if len(pr_size_bottom) == 0:
    #         pr_size_bottom = ['Bottom:' + i.text for i in drop_down[1].find_all(
    #             'option') if i.text != 'Виберіть опцію']
    #

    # for i in enumerate(pr_size_slip):
    #     pr_size[i[0]]
    # else:
    #     pr_size = (
    #         found.text.strip()
    #         if (found := soup.find(class_='pa_size-child'))
    #         else ['']
    #     )

    if (pr_name := soup.find(class_='product_title entry-title')) is not None:
        pr_name = pr_name.text.strip()
    elif (pr_name := soup.find
        (class_='woocommerce-product-details__short-description')) is not \
            None:
        pr_name = pr_name.text.strip()
    else:
        pr_name = 'Пусто'

    get_form = (f.get('data-product_variations')
                if (f := soup.find(attrs={'class': 'variations_form cart'}))
                else '')
    if (c := (re.findall('"display_price":(\d+)', get_form))):
        pr_price = c[0] + '₴'
    elif (pr_price := soup.find(
            class_='woocommerce-Price-amount amount')) is not None:
        pr_price = pr_price.text
    elif (pr_price := soup.find(class_='p-qty')) is not None:
        pr_price = pr_price.find_previous_sibling().text
    else:
        pr_price = 'Пусто'

    old_price = '' if (o_price[0] + '₴' if
                       len(o_price := re.findall('"display_regular_price":('
                                                 '\d+)', get_form)) != 0
                       else '') == pr_price else o_price[0] + '₴' \
        if len(o_price) != 0 else ''

    pr_id = (
        found.text
        if (found := soup.find(attrs={'class': 'sku'}))
        else 'ПустоИд'
    )
    for size_ in pr_size:
        pr_data.append(
            {
                'url': url,
                'name': pr_name,
                'old_price': old_price,
                'price': pr_price,
                'size': ' '.join(i for i in size_) if size_ != 'відсутній' else
                size_,
                'id': pr_id,
            }
        )
    # print(pr_data, datetime.datetime.now() - time_, url)
    return pr_data


async def pr_urls_async():
    urls_ = get_nav_urls()
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls_:
            tasks.append(asyncio.create_task(get_prod_urls(url, session)))

        results = await asyncio.gather(*tasks)
        # Достаем ссылки на продукты и отбираем повторы
        print('len:', len(list(set([item for sublist in results for item in
                                    sublist]))))
        print(list(set([item for sublist in results for item in sublist])))
        return list(set([item for sublist in results for item in sublist]))


async def get_data(pr_urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in pr_urls:
            tasks.append(asyncio.create_task(get_pr_data(url, session)))

        results = await asyncio.gather(*tasks)
        return list([item for sublist in results for item in sublist])


FILE_PATH_PARS = ''


def csv_writer(path=FILE_PATH_PARS, file_name='testdata'):
    pr_urls = asyncio.run(pr_urls_async())
    pr_data_ = asyncio.run(get_data(pr_urls))

    pr_data = sorted(pr_data_, key=lambda x: x['name'])

    with open(f'{path}{file_name}.csv', mode='w', newline='',
              encoding='utf8') as product_date:
        fieldnames = ['Название', 'Артикул', 'Цена', 'Старая цена',
                      'Ссылка', 'Размер', 'TY']
        product_date_writer = csv.DictWriter(product_date,
                                             fieldnames=fieldnames)
        product_date_writer.writeheader()
        for pr in pr_data:
            product_date_writer.writerow({'Название': pr.get('name'),
                                          'Артикул': pr.get('id'),
                                          # 'Наличие': '',
                                          'Цена': pr.get('price'),
                                          'Старая цена': pr.get('old_price'),
                                          'Ссылка': pr.get('url'),
                                          'Размер': pr.get('size'),
                                          })

    # return [pr_urls, pr_data]
    return f'Создан {file_name} в {path}'


if __name__ == '__main__':
    # time = datetime.datetime.now()
    # print(time)
    # a = asyncio.run(csv_writer())
    a = csv_writer()
    # a = asyncio.run(get_data(['https://totalfit.com.ua/product/tws5-w2/']))
    # print(datetime.datetime.now() - time)
