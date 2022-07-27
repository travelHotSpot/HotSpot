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

def imgandtext(category, typeXPATH, lastPage):
    path = f'{PROJECT_DIR}\\' + category + '_imgtext\\'
    if not os.path.isdir(path):
        os.mkdir(path)
    DOWNLOAD_DIR = path
    chrome = generate_chrome(
        driver_path=driver_path,
        headless=False,
        download_path=DOWNLOAD_DIR)
    chrome.maximize_window()
    url = 'https://api.visitkorea.or.kr/main.do'
    chrome.get(url)
    chrome.find_element(By.XPATH, '/html/body/strong/strong/div/section/header/aside/ul/li[2]/a/img').click() # 로그인 창 클릭
    time.sleep(random.randint(2, 3)) # 창변환 기다림
    elm = chrome.find_element(By.XPATH, '/html/body/form/div/section/section[2]/div[2]/div/ul/li[1]/input')
    elm.send_keys('hsj4436@pusan.ac.kr')
    elm = chrome.find_element(By.XPATH, '/html/body/form/div/section/section[2]/div[2]/div/ul/li[2]/input')
    elm.send_keys('Hotspot123!')
    chrome.find_element(By.XPATH, '/html/body/form/div/section/section[2]/div[2]/div/input').click() # 로그인 버튼 클릭
    time.sleep(random.randint(3, 4)) # 창변환 기다림
    chrome.find_element(By.XPATH, '/html/body/strong/strong/div/section/header/div[1]/nav/ul/li[3]/a/img').click() # 맞춤형 데이터 클릭
    time.sleep(random.randint(3, 4)) # 창변환 기다림
    chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/form/fieldset/div/div/table/tbody/tr[1]/td/input[1]').click() # 전체 클릭 취소
    time.sleep(random.randint(1, 2)) # 창변환 기다림
    chrome.find_element(By.XPATH, typeXPATH).click() # 관광지 데이터 클릭
    chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/form/fieldset/div/table[2]/tbody/tr/td/input[2]').click() # 검색 버튼 클릭
    time.sleep(random.randint(2, 3)) # 창변환 기다림
    chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[4]/div/select[2]').click()  # 보기 방식
    time.sleep(random.randint(2, 3))  # 창변환 기다림
    chrome.find_element(By.XPATH,
                        '/html/body/div[2]/section/section[2]/div[4]/div/select[2]/option[7]').click()  # 200개씩 보기 클릭
    chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[4]/div/input[2]').click()  # 보기 클릭

    isChecked = False
    firstPage = int(input("처음 시작 페이지 설정 (1이면 처음부터) : "))
    page = firstPage # 다운로드 시작 페이지 설정 가능
    if(page != 1): # 시작 페이지를 다르게 설정했을 때
        if(page % 10 == 0):
            pagdiv = page // 10 -1
            for i in range(pagdiv):
                chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[6]/a[3]/img').click()  # 다음 페이지
                time.sleep(random.randint(2, 3))  # 창변환 기다림
            chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[6]/span/a[9]').click()  # 마지막 페이지 클릭
            time.sleep(random.randint(2, 3))  # 창변환 기다림
        else:
            pagdiv = page // 10
            for i in range(pagdiv):
                chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[6]/a[3]/img').click()  # 다음 페이지
                time.sleep(random.randint(2, 3))  # 창변환 기다림
            cnt = page % 10 -1
            nextpageXPATH = '/html/body/div[2]/section/section[2]/div[6]/span/a[' + str(cnt) + ']'
            chrome.find_element(By.XPATH, nextpageXPATH).click()
            time.sleep(random.randint(2, 3))  # 창변환 기다림

    endPage = lastPage + 1
    for i in range(page, endPage):
        print('현재 페이지 :', page)
        if isChecked:
            chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[2]/ul/li[2]/a/img').click()  # 텍스트 다운로드
            time.sleep(random.randint(5, 6))  # 창변환 기다림
            chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[2]/ul/li[3]/a/img').click()  # 이미지 다운로드
            time.sleep(random.randint(80, 90))  # 창변환 기다림
            nextPage = page % 10
            if nextPage == 0:
                chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[6]/a[3]/img').click()
            else :
                nextpageXPATH = '/html/body/div[2]/section/section[2]/div[6]/span/a[' + str(nextPage) + ']'
                chrome.find_element(By.XPATH, nextpageXPATH).click()
            page += 1
            time.sleep(random.randint(2, 3))  # 창변환 기다림

        else: # 설문조사
            chrome.find_element(By.XPATH,
                                '/html/body/div[2]/section/section[2]/div[2]/ul/li[2]/a/img').click()  # 텍스트 다운로드
            time.sleep(random.randint(2, 3))  # 창변환 기다림
            chrome.find_element(By.XPATH,
                                '/html/body/div[2]/section/section[2]/div[3]/form/div/dl/dd[1]/input[2]').click()  #웹사이트
            elm = chrome.find_element(By.XPATH,
                                '/html/body/div[2]/section/section[2]/div[3]/form/div/dl/dd[2]/textarea')  # 활용내용
            elm.send_keys("졸업과제 웹페이지 활용")
            chrome.find_element(By.XPATH,
                                '/html/body/div[2]/section/section[2]/div[3]/form/div/div/a').click()
            time.sleep(random.randint(5, 6))  # 창변환 기다림
            chrome.find_element(By.XPATH,
                                '/html/body/div[2]/section/section[2]/div[2]/ul/li[3]/a/img').click()  # 이미지 다운로드
            time.sleep(random.randint(80, 90))  # 창변환 기다림

            nextPage = page % 10
            if nextPage == 0:
                chrome.find_element(By.XPATH, '/html/body/div[2]/section/section[2]/div[6]/a[3]/img').click()
            else:
                try:
                    nextpageXPATH = '/html/body/div[2]/section/section[2]/div[6]/span/a[' + str(nextPage) + ']'
                    chrome.find_element(By.XPATH, nextpageXPATH).click()
                except:
                    if nextPage == lastPage:
                        print('모든 작업이 끝났습니다.')
                        break
                page += 1
            time.sleep(random.randint(2, 3))  # 창변환 기다림
            isChecked = True

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
    path = f'{PROJECT_DIR}\\populartourspot\\'
    if not os.path.isdir(path):
        os.mkdir(path)
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
    path = f'{PROJECT_DIR}\\picture\\'
    if not os.path.isdir(path):
        os.mkdir(path)
    DOWNLOAD_DIR = f'{PROJECT_DIR}\\picture\\'
    chrome = generate_chrome(
        driver_path=driver_path,
        headless=False,
        download_path=DOWNLOAD_DIR)
    chrome.maximize_window()
    num = int(input("검색할 횟수 : "))
    img = []
    for i in range(num):
        img.append(input("찾고 싶은 관광지 이름을 입력하세요 : "))
    for i in range(num):
        url = 'https://unsplash.com/'
        chrome.get(url)
        search = img[i]
        elm = chrome.find_element(By.XPATH, '/html/body/div/div/header/nav/div[2]/form/div[1]/input')
        elm.send_keys(search)
        elm.send_keys(Keys.RETURN)
        time.sleep(random.randint(2, 3))
        try:
            chrome.find_element(By.XPATH, '/html/body/div/div/div[2]/div[4]/div[1]/div/div/div/div[1]/figure[1]/div/div[1]/div/div/a/div/div[2]/div/img').click()
            time.sleep(random.randint(2, 3))
            chrome.find_element(By.XPATH, '/html/body/div[4]/div/div/div[4]/div/div/div[1]/div[1]/header/div[2]/div[3]/div/a/span').click()
            time.sleep(random.randint(5, 6))
            filename = max([DOWNLOAD_DIR + '\\' + f for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getctime)
            shutil.move(os.path.join(DOWNLOAD_DIR, filename), DOWNLOAD_DIR + '//' + search + '.jpg')
        except:
            print("없는 이미지 입니다.")




def trend():
    path = f'{PROJECT_DIR}\\trend\\'
    if not os.path.isdir(path):
        os.mkdir(path)

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


command = input("하고 싶은 작업 입력 (1.이미지텍스트, 2.인기관광지, 3.추가이미지, 4.트렌드) : " )
if command == '이미지텍스트' or command == '1':
    second = input("1.관광지, 2.문화시설, 3.축제공연행사 : ")
    if second == '관광지' or second == '1':
        imgandtext("touristspot",'/html/body/div[2]/section/section[2]/form/fieldset/div/div/table/tbody/tr[1]/td/input[2]',60)
    elif second == '문화시설' or second == '2':
        imgandtext("culturalfacilities",'/html/body/div[2]/section/section[2]/form/fieldset/div/div/table/tbody/tr[1]/td/input[3]',11)
    else:
        imgandtext("festival",'/html/body/div[2]/section/section[2]/form/fieldset/div/div/table/tbody/tr[1]/td/input[4]',6)

elif command == '인기관광지' or command == '2':
    popularTouristspot()
elif command == '이미지' or command == '3':
    picture()
else:
    trend()

