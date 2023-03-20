import asyncio
import csv
import datetime
import re
from time import sleep
import aiohttp
import requests
from bs4 import BeautifulSoup
import fake_useragent

user = fake_useragent.UserAgent().random
# login = 'login'
# password = 'password'
headers = {'user-agent': user}


def get_nav_urls():
    site_url = 'https://totalfit.com.ua/'
    request = requests.get(site_url, headers=headers)
    soup = BeautifulSoup(request.content, 'lxml')
    list_urls_in_nav = []
    urls_in_nav = soup.find('nav', attrs={'id': 'main-nav-wrap'}).find_all('ul')
    for i in urls_in_nav:
        for l in i.find_all('a'):
            temp = l.get('href')
            if 'product-category' in temp and temp not in list_urls_in_nav:
                list_urls_in_nav.append(l.get('href'))
    return list_urls_in_nav


# unnecessary = ['https://totalfit.com.ua/product-category/accessories-uk/',
#                'https://totalfit.com.ua/product-category/iceland-uk/',
#                'https://totalfit.com.ua/product-category/cycling-uk/',
#                'https://totalfit.com.ua/product-category/for-children-uk/',
#                'https://totalfit.com.ua/product-category/thermo-uk/',
#                'https://totalfit.com.ua/product-category/swimsuits-uk/',
#                'https://totalfit.com.ua/product-category/casual-uk/',
#                ]

async def get_html(url):
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url=url, headers=headers, ssl=False,
    #                            verify=False) as resp:
    #
    #         return BeautifulSoup(await resp.text(), "lxml")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, ssl=False, verify=False
                                   ) as resp:
                for i in range(5):
                    if resp.ok:
                        return BeautifulSoup(await resp.text(), "lxml")
                    else:
                        await asyncio.sleep(2)
                return BeautifulSoup(await resp.text(), "lxml")
    except:
        request = requests.get(url, headers=headers)
        # soup = BeautifulSoup(request.text, 'lxml')
        return BeautifulSoup(request.text, 'lxml')


async def get_prod_urls(url):
    pr_urls = []
    page = 1
    while page:
        # try:
        request = await get_html(url + f'/page/{page}')

        # soup = BeautifulSoup(request, 'lxml')
        soup = request
        pr_on_url = soup.find('div', class_='wpf-search-container')
        if pr_on_url is None:
            page = 0
            continue
        else:
            pr_on_url = pr_on_url.find('ul')
        get_prod_urls_in_page = pr_on_url.find_all('li')
        # prod_urls_in_page = [i.find('a').get('href') for i in get_prod_urls_in_page]
        prod_urls_in_page = [i.find('a').get('href')
                             for i in get_prod_urls_in_page if
                             'product-category' not in i.find('a').get('href')]
        pr_urls += prod_urls_in_page
        page += 1
    return pr_urls


async def get_pr_data(url):
    pr_data = []
    request = await get_html(url)
    soup = request
    # soup = BeautifulSoup(request, 'lxml')
    if not soup.find('nav'):
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')
    #
    drop_down = soup.find_all('select')
    if len(drop_down) == 2:

        pr_size = [i.text for i in drop_down[0].find_all('option') if
                   i.text != 'Виберіть опцію']
        if 'Оцінка…' in pr_size:
            pr_size = ['Відсутній']

    elif len(drop_down) >= 3:
        get_form = soup.find(attrs={'class': 'variations_form cart'}).get(
            'data-product_variations')
        pr_size_top = ['Top:' + str(i).upper()
                       for i in re.findall(r'"attribute_pa_top-size":"(\w+)',
                                           get_form)
                       ]

        if len(pr_size_top) == 0:
            pr_size_top = ['Top:' + i.text for i in drop_down[0].find_all
            ('option') if i.text != 'Виберіть опцію']

        pr_size_bottom = ['Bottom:' + str(i).upper()
                          for i in
                          re.findall(r'"attribute_pa_bottom-size":"(\w+)',
                                     get_form)
                          ]
        if len(pr_size_bottom) == 0:
            pr_size_bottom = ['Bottom:' + i.text for i in drop_down[1].find_all(
                'option') if i.text != 'Виберіть опцію']

        if len(pr_size_top) > len(pr_size_bottom):
            pr_size = []
            for i in enumerate(pr_size_bottom):
                pr_size += [[pr_size_top[i[0]], pr_size_bottom[i[0]]]]
            pr_size += [[pr_size_top[-1]]]
        elif len(pr_size_top) < len(pr_size_bottom):
            pr_size = []
            for i in enumerate(pr_size_top):
                pr_size += [[pr_size_top[i[0]], pr_size_bottom[i[0]]]]
            pr_size += [[pr_size_bottom[-1]]]
        else:
            pr_size = []
            for i in enumerate(pr_size_top):
                pr_size += [[pr_size_top[i[0]], pr_size_bottom[i[0]]]]
    else:
        pr_size = (
            found.text.strip()
            if (found := soup.find(class_='pa_size-child'))
            else ['']
        )
    # todo проблема в запросах размера https://totalfit.com.ua/product/103759/
    # pr_name = (
    #     found.find('p').text
    #     if (found := soup.find(
    #         class_='woocommerce-product-details__short-description'))
    #     else 'Пусто'
    # )
    # pr_name = (
    #     found.text
    #     if (found := soup.find(class_='product_title entry-title'))
    #     else 'Пусто'
    # )
    if (pr_name := soup.find(class_='product_title entry-title')) is not None:
        pr_name = pr_name.text.strip()
    elif (pr_name := soup.find
        (class_='woocommerce-product-details__short-description')) is not \
            None:
        pr_name = pr_name.text.strip()
    else:
        pr_name = 'Пусто'

    # if (pr_price := soup.find(
    #         class_='woocommerce-Price-amount amount')) is not None:
    #     pr_price = pr_price.text
    # elif (pr_price := soup.find(class_='p-qty')) is not None:
    #     pr_price = pr_price.find_previous_sibling().text
    # else:
    #     pr_price = 'Пусто
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

    pr_id = (
        found.text
        if (found := soup.find(attrs={'class': 'sku'}))
        else 'ПустоИд'
    )
    for size in pr_size:
        pr_data.append(
            {
                'url': url,
                'name': pr_name,
                'price': pr_price,
                'size': size,
                'id': pr_id + f'-{size}',
            }
        )

    return pr_data


async def pr_urls_async():
    urls_ = get_nav_urls()
    tasks = []

    for url in urls_:
        tasks.append(asyncio.create_task(get_prod_urls(url)))

    results = await asyncio.gather(*tasks)
    # Достаем ссылки на продукты и отбираем повторы
    await asyncio.sleep(0.25)

    return list(set([item for sublist in results for item in sublist]))


async def get_data(pr_urls):
    tasks = []

    for url in pr_urls:
        tasks.append(asyncio.create_task(get_pr_data(url)))

    results = await asyncio.gather(*tasks)
    await asyncio.sleep(0.25)
    return list([item for sublist in results for item in sublist])


FILE_PATH_PARS = ''


def csv_writer(path=FILE_PATH_PARS, file_name='testdata'):
    print('1')
    pr_urls = asyncio.run(pr_urls_async())
    print(len(pr_urls))
    print('2')
    pr_data = asyncio.run(get_data(pr_urls))
    print('3')

    with open(f'{path}{file_name}.csv', mode='w', newline='', encoding='utf8') \
            as product_date:
        fieldnames = ['Название', 'Артикул', 'Наличие',
                      'Цена', 'Ссылка', 'Размер', 'TY']
        product_date_writer = csv.DictWriter(product_date,
                                             fieldnames=fieldnames)
        product_date_writer.writeheader()
        for pr in pr_data:
            product_date_writer.writerow({'Название': pr.get('name'),
                                          'Артикул': pr.get('id'),
                                          'Наличие': '',
                                          'Цена': pr.get('price'),
                                          'Ссылка': pr.get('url'),
                                          'Размер': pr.get('size'),
                                          })

    # return [pr_urls, pr_data]
    return f'Создан {file_name} в {path}'


if __name__ == '__main__':
    time = datetime.datetime.now()
    print(time)
    a = csv_writer()
    print(datetime.datetime.now() - time)

# import requests
# from bs4 import BeautifulSoup
# request = requests.get('https://totalfit.com.ua/product/t1-p73/')
# soup = BeautifulSoup(request.text, 'html.parser')
