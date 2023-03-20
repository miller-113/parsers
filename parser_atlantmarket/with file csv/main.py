import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def parse_file(path, csv_file_name):
    s = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option('prefs', {
        'download.default_directory': path,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing_for_trusted_sources_enabled': False,
        'safebrowsing.enabled': False
    })
    # options.add_experimental_option()
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
    browser.get('https://atlantmarket.com.ua/price1/csv/atlantmarket-price.csv')
    # link = browser.find_element(By.LINK_TEXT, 'Atlantmarket-price.csv')
    # link.click()
    time.sleep(3)
    
    files = os.listdir(path)
    last_added_file = sorted(files, key=lambda x: os.path.getmtime(path + x))[
        -1]
    try:
        os.rename(path + last_added_file, path + csv_file_name)
    except FileExistsError:
        os.remove(path + csv_file_name)
        os.rename(path + last_added_file, path + csv_file_name)
