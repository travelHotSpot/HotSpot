# main.py
from openpyxl import Workbook
import sys
import os
import time
import random
from datetime import datetime
from selenium.webdriver.common.by import By
from chromedriver import generate_chrome


PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}\\download\\'
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


url = 'https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=25c89d50-1e55-11eb-a4e6-a9a03a61580b'

chrome.maximize_window()
chrome.get(url)
time.sleep(random.randint(1, 3))

elm = chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[2]/div[4]/div[2]/ul/li[2]/div[1]/span/label/span').click() # 클릭
elm = chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[2]/div[5]/div[1]/div/ul/li/a/span').click() # 미리보기
time.sleep(random.randint(5, 10))


wb = Workbook()
ws = wb.active
ws.title = '국내 여행 TOP10'

columns = ['SEQ_NO', 'ALL_KWRD_RANK_CO', 'SRCHWRD_NM', 'UPPER_CTGRY_NM', 'LWPRT_CTGRY_NM', 'AREA_NM',
           'MOBILE_SCCNT_VALUE','PC_SCCNT_VALUE', 'SCCNT_SM_VALUE', 'SCCNT_DE']
ws.append(columns)


tablexpath = '/html/body/div[2]/div[2]/div/div/div[2]/div[5]/div[2]/table/tbody/'

trindx = 1

for i in range(10):
    tableColumns = []
    index = trindx
    xpath = tablexpath + 'tr[' + str(trindx) +']/'
    tdindx = 1
    for j in range(10):
        fullxpath = xpath + 'td[' + str(tdindx) + ']'
        tabletext = chrome.find_element(By.XPATH, fullxpath).text
        tableColumns.append(tabletext)
        tdindx = tdindx + 1

    ws.append(tableColumns)
    trindx = trindx + 2

date = chrome.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div[2]/div[5]/div[2]/table/tbody/tr[1]/td[10]').text
wb.save(".\\trend\\trend10" + date + ".xlsx")
wb.close()
input('대기')