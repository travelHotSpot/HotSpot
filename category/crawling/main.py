# main.py
from selenium.webdriver.common.keys import Keys
import sys
import os
import time
import shutil
from chromedriver import generate_chrome
from openpyxl import Workbook
from selenium.webdriver.common.by import By
import random

PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
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

def festival():
    DOWNLOAD_DIR = f'{PROJECT_DIR}\\festival\\'
    chrome = generate_chrome(
        driver_path=driver_path,
        headless=False,
        download_path=DOWNLOAD_DIR)
    chrome.maximize_window()
    url = 'https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp'
    chrome.get(url)
    elm = chrome.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div[1]/ul/li[2]/form/a/span')
    elm.click()
    time.sleep(random.randint(6, 10))
    chrome.close()

def region(Xpath, chrome):
    chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[1]/a').click()  # 지역 선택창 클릭
    time.sleep(random.randint(2, 3))
    elm = chrome.find_element(By.XPATH, Xpath)
    regionname = elm.text
    elm.click()
    print(regionname)
    chrome.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[3]/div/a[2]').click()  # 확인 창 클릭
    time.sleep(random.randint(2, 3))
    chrome.find_element(By.XPATH,  '/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[6]/div[9]/div[1]/div[1]/ul/li[3]/a').click()  # 인기 관광지 전체 선택
    chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[6]/div[9]/div[1]/div[1]/div[2]/a').click()  # 인기 관광지 세부 선택
    time.sleep(random.randint(2, 3))
    chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[6]/div[9]/div[1]/div[1]/div[2]/ul/li[2]/p/a').click()  # 데이터 다운로드 클릭
    time.sleep(random.randint(2, 3))
    chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[8]/div[2]/div[3]/a[1]').click()  # 제출 클릭
    time.sleep(random.randint(3, 5))

def popularTouristspot():
    DOWNLOAD_DIR = f'{PROJECT_DIR}\\populartourspot\\'
    print(DOWNLOAD_DIR)
    chrome = generate_chrome(
        driver_path=driver_path,
        headless=False,
        download_path=DOWNLOAD_DIR)
    chrome.maximize_window()

    url = 'https://datalab.visitkorea.or.kr/datalab/portal/mbr/getMbrLoginForm.do'
    chrome.get(url)
    time.sleep(random.randint(2, 3))
    elm = chrome.find_element(By.ID,'mbrId')
    elm.send_keys('1dolcong@naver.com')
    elm = chrome.find_element(By.ID,'mbrPw')
    elm.send_keys('hotspot123!')
    elm.send_keys(Keys.RETURN)
    time.sleep(random.randint(2, 3))
    chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[7]/div[1]/ul/li[1]/div/a').click() #지역별 로고 클릭
    time.sleep(random.randint(2, 3))
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[1]', chrome) #서울
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[2]', chrome) #부산
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[3]', chrome) #대구
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[4]', chrome) #인천
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[5]', chrome) #광주
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[6]', chrome) #대전
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[7]', chrome) #울산
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[8]', chrome) #세종
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[1]/a[9]', chrome) #경기
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]/a[1]', chrome) #강원
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]/a[2]', chrome) #충청북도
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]/a[3]', chrome) #충청남도
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]/a[4]', chrome) #전라북도
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]/a[5]', chrome) #전라남도
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]/a[6]', chrome) #경상북도
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]/a[7]', chrome) #경상남도
    region('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]/a[8]', chrome) #제주

def picture():
    DOWNLOAD_DIR = f'{PROJECT_DIR}\\picture\\'
    chrome = generate_chrome(
        driver_path=driver_path,
        headless=False,
        download_path=DOWNLOAD_DIR)
    chrome.maximize_window()

    url = 'https://unsplash.com/'
    chrome.set_window_size(600, 664)
    chrome.get(url)
    search = input("찾고 싶은 관광지 이름을 입력하세요 : ")
    time.sleep(random.randint(2, 4))
    elm = chrome.find_element(By.XPATH, '/html/body/div/div/div[2]/nav/div[2]/form/div/input')
    elm.send_keys(search)
    elm.send_keys(Keys.RETURN)

    elm = chrome.find_element(By.CLASS_NAME, 'YVj9w').click()
    time.sleep(random.randint(2, 4))

    elm = chrome.find_element(By.CLASS_NAME, 'wl5gA').click()
    time.sleep(random.randint(2, 3))

    filename = max([DOWNLOAD_DIR + '\\' + f for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getctime)
    shutil.move(os.path.join(DOWNLOAD_DIR, filename), DOWNLOAD_DIR + '//' + search + '.jpg')
    chrome.close()

def trend():
    DOWNLOAD_DIR = f'{PROJECT_DIR}\\trend\\'
    chrome = generate_chrome(
        driver_path=driver_path,
        headless=False,
        download_path=DOWNLOAD_DIR)
    chrome.maximize_window()

    url = 'https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=25c89d50-1e55-11eb-a4e6-a9a03a61580b'

    chrome.maximize_window()
    chrome.get(url)
    time.sleep(random.randint(1, 3))

    chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[2]/div[4]/div[2]/ul/li[2]/div[1]/span/label/span').click()  # 클릭
    chrome.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[2]/div[5]/div[1]/div/ul/li/a/span').click()  # 미리보기
    time.sleep(random.randint(5, 10))
    wb = Workbook()
    ws = wb.active
    ws.title = '국내 여행 TOP10'
    columns = ['SEQ_NO', 'ALL_KWRD_RANK_CO', 'SRCHWRD_NM', 'UPPER_CTGRY_NM', 'LWPRT_CTGRY_NM', 'AREA_NM',
               'MOBILE_SCCNT_VALUE', 'PC_SCCNT_VALUE', 'SCCNT_SM_VALUE', 'SCCNT_DE']
    ws.append(columns)
    tablexpath = '/html/body/div[2]/div[2]/div/div/div[2]/div[5]/div[2]/table/tbody/'
    trindx = 1
    for i in range(10):
        tableColumns = []
        xpath = tablexpath + 'tr[' + str(trindx) + ']/'
        tdindx = 1
        for j in range(10):
            fullxpath = xpath + 'td[' + str(tdindx) + ']'
            tabletext = chrome.find_element(By.XPATH, fullxpath).text
            tableColumns.append(tabletext)
            tdindx = tdindx + 1

        ws.append(tableColumns)
        trindx = trindx + 2

    date = chrome.find_element(By.XPATH,
                               '/html/body/div[2]/div[2]/div/div/div[2]/div[5]/div[2]/table/tbody/tr[1]/td[10]').text
    wb.save(".\\trend\\trend10" + date + ".xlsx")
    wb.close()






command = input("하고 싶은 작업 입력 (1.축제, 2.인기관광지, 3.그림, 4.트렌드) : " )
if command == '축제':
    festival()
elif command == '인기관광지':
    popularTouristspot()
elif command == '그림':
    picture()
else:
    trend()

