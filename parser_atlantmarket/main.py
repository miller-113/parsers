import csv
import time
from multiprocessing import Pool
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

PR_DATA = []
CHECK = []

count_products_in_invoice = 5000


def get_data(l, pr_data=None, check=None):
    global all_products, browser
    if check is None:
        check = CHECK
    if pr_data is None:
        pr_data = PR_DATA
    pr_data1 = []
    try:

        s = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')

        options.add_argument("--window-size=1920,1080")

        browser = webdriver.Chrome(service=s, options=options)

        browser.get('https://atlantmarket.com.ua/cabinet/')
        login_form = browser.find_elements(By.CLASS_NAME,
                                           'registration-form__input')
        login_form[0].clear()

        login_form[0].send_keys('login')
        login_form[1].clear()
        login_form[1].send_keys('password')
        browser.find_element(By.CLASS_NAME,
                             'registration-form__button').find_element(
            By.TAG_NAME, 'input').click()
        time.sleep(5)

        groups_of_pr = browser.find_element(By.XPATH,
                                            '//*[@id="horizontal-multilevel-menu"]/div[1]/div[2]/div/div/div/div') \
            .find_elements(By.TAG_NAME, 'a')
        groups_of_pr = list(filter(lambda x: x.get_attribute(
            'class') == 'second_lev' or x.get_attribute(
            'class') == 'first_lev' or x.get_attribute(
            'class') == 'third_lev', groups_of_pr))
        ln_pr = len(groups_of_pr)
        if l == 1:
            groups_of_pr = groups_of_pr[:ln_pr // 6]
        elif l == 2:
            groups_of_pr = groups_of_pr[ln_pr // 6:ln_pr // 6 * 2]
        elif l == 3:
            groups_of_pr = groups_of_pr[ln_pr // 6 * 2:ln_pr // 6 * 3]
        elif l == 4:
            groups_of_pr = groups_of_pr[ln_pr // 6 * 3:ln_pr // 6 * 4]
        elif l == 5:
            groups_of_pr = groups_of_pr[ln_pr // 6 * 4:ln_pr // 6 * 5]
        elif l == 6:
            groups_of_pr = groups_of_pr[ln_pr // 6 * 5:]

        all_products = browser.find_element(By.XPATH,
                                            '//*[@id="wrapper"]/main/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[1]/div/span').text.split()[
            -1]

        while True:
            t = time.monotonic()
            for i in groups_of_pr:
                if time.monotonic() - t > 900:
                    break
                i.click()

                time.sleep(1)
                ch = 0
                try:
                    while True:
                        pagination = browser.find_element(By.XPATH,
                                                          '//*[@id="wrapper"]/main/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[1]/div/span').text.split()
                        p1 = pagination[3]
                        p2 = pagination[-1]

                        if ch == 0:
                            browser.find_element(By.XPATH,
                                                 '//*[@id="wrapper"]/main/div[2]/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div[1]').click()
                        if int(p1) >= int(p2):
                            break
                        if time.monotonic() - t > 500:
                            break
                        else:
                            s = lambda x: max(0, min(x, 50))
                            browser.find_element(By.TAG_NAME, 'body').send_keys(
                                Keys.DOWN * (s(int(p2) - int(p1))))

                        ch += 1

                    soup = BeautifulSoup(browser.page_source, 'lxml')
                    all_product = soup.find('div',
                                            class_='table-body__inner').find_all(
                        'div', class_='table-row')
                    for i in all_product:
                        pr_cells = i.find_all('div', class_='table-cell')
                        id = pr_cells[1].text.strip()
                        id_articul = pr_cells[2].text.strip()
                        status = pr_cells[3].text.strip()
                        name = pr_cells[4].text.strip()
                        certificate = pr_cells[5].text.strip()
                        count_stock = pr_cells[6].text.strip()
                        price_opt = pr_cells[7].text.strip()
                        price_rrc = pr_cells[8].text.strip()
                        pr_data1.append({
                            'id': id,
                            'id_articul': id_articul,
                            'status': status,
                            'name': name,
                            'certificate': certificate,
                            'count_stock': count_stock,
                            'price_opt': price_opt,
                            'price_rrc': price_rrc,
                        })
                except:
                    continue

            print(
                f'{l} Сбор товаров завершен в {", ".join([i.text for i in groups_of_pr])}. Колл. товаров в категории {len(pr_data1)}')
            break
    except Exception as e:
        print(e)

    finally:
        browser.close()
        return [pr_data1, all_products]


def csv_writer(path_to_save, file_name):
    global all_products_onpage

    while True:
        try:
            global task
            q = 0
            p = Pool(3)
            _list = [1, 2, 3, 4, 5, 6]
            checker = []
            pr_data = []
            for task in p.map(get_data, _list):
                pr_data.append(task[0])
            all_products_onpage = task[1]
            for task_data in pr_data:
                for pr in task_data:
                    q += 1
            print('Собранные товары', q)
            print('Сколько на главной:', all_products_onpage)
            if int(q) <= int(all_products_onpage) and int(q) <= \
                    count_products_in_invoice:
                continue
            else:

                with open(f'{path_to_save}{file_name}.csv', 'w',
                          encoding='utf8', newline='') as f:
                    fieldnames = ['Код', 'Артикул', 'Статус', 'Найменовання',
                                  'Сертифiкат', 'Залишок', 'Опт', 'РРЦ',
                                  'TY']
                    product_date_writer = csv.DictWriter(f,
                                                         fieldnames=fieldnames)
                    product_date_writer.writeheader()
                    for task_data in pr_data:
                        for pr in task_data:
                            if pr not in checker:
                                checker.append(pr)
                                product_date_writer.writerow(
                                    {'Код': pr.get('id'),
                                     'Артикул': pr.get('id_articul'),
                                     'Статус': pr.get('status'),
                                     'Найменовання': pr.get('name'),
                                     'Сертифiкат': pr.get('certificate'),
                                     'Залишок': pr.get('count_stock'),
                                     'Опт': pr.get('price_opt'),
                                     'РРЦ': pr.get('price_rrc')})
                            else:
                                continue
                    print(len(checker), ': count products without duplicates')
            return f'Файл: {file_name} записан в {path_to_save}'
        except Exception as e:
            print(e)
            continue
