# main.py
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from chromedriver import generate_chrome
from selenium.webdriver.common.keys import Keys
import sys
import os
import time
import shutil
import random



PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}\\picture\\'
driver_path = f'{PROJECT_DIR}\\lib\\'

platform = sys.platform
if platform == 'darwin':
    print('System platform : Darwin')
    driver_path += 'chromedriverMac'
elif platform == 'linux':
    print('System platform : Linux')
    driver_path += 'chromedriverLinux'
elif platform == 'win32':
    print('System platform : Window')
    driver_path += 'chromedriverWindow'
else:
    print(f'[{sys.platform}] not supported. Check your system platform.')
    raise Exception()

# 크롬 드라이버 인스턴스 생성
chrome = generate_chrome(
    driver_path=driver_path,
    headless=False,
    download_path=DOWNLOAD_DIR)



url = 'https://unsplash.com/'
chrome.set_window_size(600,664)
chrome.get(url)
search = '해운대'
time.sleep(random.randint(2,4))
elm = chrome.find_element(By.XPATH, '/html/body/div/div/div[2]/nav/div[2]/form/div/input')
elm.send_keys(search)
elm.send_keys(Keys.RETURN)

elm = chrome.find_element(By.CLASS_NAME, 'YVj9w').click()
time.sleep(random.randint(2, 4))

elm = chrome.find_element(By.CLASS_NAME, 'wl5gA').click()
time.sleep(random.randint(2, 3))

filename = max([DOWNLOAD_DIR + '\\' + f for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getctime)
shutil.move(os.path.join(DOWNLOAD_DIR, filename), DOWNLOAD_DIR + '//' +search+'.jpg')
