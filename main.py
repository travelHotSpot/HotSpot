# main.py
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pickle
import sys
import os
import time

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

url = 'https://www.mcst.go.kr/kor/s_culture/festival/festivalList.jsp'
chrome.get(url)
elm = chrome.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/div[1]/ul/li[2]/form/a/span')
elm.click()
time.sleep(1)

url = 'https://datalab.visitkorea.or.kr/datalab/portal/mbr/getMbrLoginForm.do'
chrome.get(url)
time.sleep(3)
elm = chrome.find_element_by_id('mbrId')
elm.send_keys('1dolcong@gmail.com')
elm = chrome.find_element_by_id('mbrPw')
elm.send_keys('shltls12!')
elm.send_keys(Keys.RETURN)
time.sleep(3)

region = chrome.find_element_by_xpath('/html/body/div[2]/div[2]/div[7]/div[1]/ul/li[1]/div/a').click()
time.sleep(2)
regiondown = chrome.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div[4]/div[2]/a[4]').click()
time.sleep(3)
surveyclick = chrome.find_element_by_xpath('/html/body/div[2]/div[2]/div[8]/div[2]/div[2]/ul/li[5]/label').click()
time.sleep(1)
surveysubmit =chrome.find_element_by_xpath('/html/body/div[2]/div[2]/div[8]/div[2]/div[3]/a[1]').click()
time.sleep(100)

# 쿠키 사용
# cookies = chrome.get_cookies()
# for cookie in cookies:
#     chrome.add_cookie((cookie))
# chrome.get('https://datalab.visitkorea.or.kr/datalab/portal/bda/getMetcoAna.do')
# time.sleep(3)

# time.sleep(3)


menu = chrome.find_element_by_xpath('/html/body/div[2]/header/div[2]/div/nav/ul/li[4]/a')
submenu = chrome.find_element_by_xpath('/html/body/div[2]/header/div[2]/div/nav/ul/li[4]/a')

time.sleep(10)

