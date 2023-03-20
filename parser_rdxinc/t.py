import asyncio
import re

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import fake_useragent

user = fake_useragent.UserAgent().random

session = requests.Session()
headers = {'user-agent': user}
URL = 'https://rdxinc.com.ua/bokserskie-perchatki-v-noks-inizio-8-un/'
urls = [
    'https://rdxinc.com.ua/bokserskie-perchatki-leone-greatest-black-12-un/',
    'https://rdxinc.com.ua/bokserskie-perchatki-v-noks-inizio-8-un/',
    'https://rdxinc.com.ua/bokserskie-perchatki-leone-revo-performance-black-12-un/',
    'https://rdxinc.com.ua/bokserskie-perchatki-leone-shock-black-10/',
    'https://rdxinc.com.ua/bokserskie-perchatki-leone-tecnico-grey-10-un/',
    'https://rdxinc.com.ua/bokserskie-perchatki-rdx-bazooka-2-0-10-un/']
option = Options()
option.add_argument("--disable-infobars")


async def reader(urls):
    browser = webdriver.Chrome('C:\webdr\chromedriver.exe',
                               chrome_options=option)

    await asyncio.sleep(5)

    for l in urls:
        browser.get(l)
        share = browser.find_elements(By.CLASS_NAME, 'hpm-item')
        for i in share:
            i.click()
            time.sleep(0.2)
            s = re.findall(
                '<div class="info-product"><b>Артикул:</b> <span itemprop="sku">(\d+)</span></div>',
                browser.page_source)
            print(s)

    browser.close()


async def main():
    task1 = asyncio.create_task(reader(urls[0]))
    task2 = asyncio.create_task(reader(urls[1]))

    await task1
    await task2


asyncio.run(main())
