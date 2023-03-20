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

# global PR_DATA
# global CHECK


pr_data1 = []

s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')

options.add_argument("--window-size=1920,1080")
# options.add_argument(True)

browser = webdriver.Chrome(service=s, options=options)
# browser.fullscreen_window()
# browser.set_window_size(1600, 1100)
# browser.minimize_window()

browser.get('https://brandinhand.com.ua/sumki-zhenskie/')
# login_form = browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[4]/div/div/div/div/div[2]/div[2]/form/div[1]/input')
# login_form = browser.find_elements(By.CLASS_NAME, 'registration-form__input')
# login_form.clear()
# login_form[0].clear()

# login_form[0].send_keys('sup@foods-body.ua')

# password_form = browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[4]/div/div/div/div/div[2]/div[2]/form/div[2]/input')

# password_form.clear()
# login_form[1].clear()
# password_form.send_keys('D3RXjAKM')
# login_form[1].send_keys('D3RXjAKM')
browser.find_element(By.XPATH, '//*[@id="mfilter-content-container"]/div[2]/div').find_elements(By.TAG_NAME, 'a')
