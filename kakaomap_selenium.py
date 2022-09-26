from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
import numpy as np
import pandas as pd


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36")

driver = webdriver.Chrome("C:/Python39/chromedriver.exe", options=chrome_options)

url = 'https://map.kakao.com/'

busan_gu = ["중구", "서구", "동구", "영도구", "부산진구", "동래구", "남구", "북구", "해운대구", "사하구", "금정구", "강서구", "연제구", "수영구", "사상구", "기장군"]

place_df = pd.DataFrame(columns=['name', 'category', 'address', 'operation_time', 'homepage', 'tel', 'tag', 'etc', 'facility', 'num_of_comments', 'avg_rate', 'url'])
comment_df = pd.DataFrame(columns=['place_name', 'nickname', 'total_comments', 'avg_rating', 'rating', 'comment', 'created_at'])
# place_df = pd.read_csv('./2_4 place_info.csv', index_col=[0])
# comment_df = pd.read_csv('./2_4 comment_info.csv', index_col=[0])

scraped_page = 0

def scrap_from_kakaomap():
    global scraped_page
    global place_df
    global comment_df

    driver.get(url)

    driver.maximize_window()
    # driver.execute_script("document.body.style.zoom='zoom 90%'")

    for gu in busan_gu:
        scraped_page = 0
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#search"))) # 명시적대기
        
        # 부산 XX구 관광지 검색
        driver.find_element_by_xpath('//*[@id="search.keyword.query"]').clear()
        driver.find_element_by_xpath('//*[@id="search.keyword.query"]').send_keys("부산 " + gu + " 관광지")
        driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
        
        sleep(1)
                
        # '장소' 클릭
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[5]/div[2]/div[1]/div[2]/ul/li[2]/a"))) # 명시적대기
        driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[1]/div[2]/ul/li[2]/a').send_keys(Keys.ENTER)
        
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="info.search.page"]/div')))
                
        while True:
            # 검색결과 페이징 1,2,3,4,5 중 hidden인 경우 마지막 페이지
            for search_page in range(1, 6):
                if search_page != 1:
                    if "HIDDEN" in driver.find_element_by_xpath('//*[@id="info.search.page.no' + str(search_page) + '"]').get_attribute("class"):
                        break
                    else:
                        driver.find_element_by_xpath('//*[@id="info.search.page.no' + str(search_page) + '"]').send_keys(Keys.ENTER)
                
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # 15개의 관광지 목록 + 광고1개
                places = soup.select('.placelist > li')
                
                # 15개의 관광지 목록 상세정보 클릭
                for i, p in enumerate(places):
                    try:
                        driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']')
                    except NoSuchElementException:
                        break
                    
                    # 광고 pass
                    if "AdItem" in driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']').get_attribute("class"):
                        continue

                    # 리뷰(댓글) 0개이면 pass
                    if int(driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[4]/a/em').text.replace(",", "")) == 0:
                        print(driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[3]/strong/a[2]').text + "리뷰 0개")
                        continue

                    # 같은 이름의 관광지가 있을 시, 리뷰와 정보를 스크랩하지 않고 continue
                    p_name = driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[3]/strong/a[2]').text
                    if not place_df[place_df["name"] == p_name].empty:
                        sleep(0.8)
                        continue
                    
                    # 주소가 부산이 아니면 continue
                    p_address = driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[2]/p[1]').text
                    if p_address != "" and not p_address.startswith("부산"):
                        sleep(0.8)
                        continue

                    # 상세정보 페이지로 탭 전환
                    driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[4]/a[1]').send_keys(Keys.ENTER)
                    driver.switch_to.window(driver.window_handles[-1])
                    
                    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="mArticle"]/div[1]')))

                    detail_page = driver.page_source
                    detail_page_soup = BeautifulSoup(detail_page, 'html.parser')
                    
                    # 장소 이름
                    place_name = detail_page_soup.select('.place_details > .inner_place > .tit_location')
                    place_name = place_name[0].text if len(place_name) != 0 else np.nan
                    
                    # 같은 이름의 관광지가 있을 시, 리뷰와 정보를 스크랩하지 않고 탈출
                    if not place_df[place_df["name"] == place_name].empty:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        sleep(1)
                        continue
                    
                    # basicInfoTop
                    # 카테고리
                    place_category = detail_page_soup.select('.place_details > .inner_place > .location_evaluation > .txt_location')
                    place_category = place_category[0].text[4:] if len(place_category) != 0 else np.nan
                    place_category = place_category.split(",")
                    
                    # basicInfo
                    # 주소
                    place_address = detail_page_soup.select('.placeinfo_default > .location_detail > .txt_address')
                    place_address = place_address[0].text.replace('\n                ', ' ') if len(place_address) != 0 else np.nan
                    
                    # 주소가 부산으로 시작하지 않으면 탈출
                    if not place_address.startswith("부산"):
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        sleep(1)
                        continue
                    
                    # 영업시간
                    operation_time = detail_page_soup.select('.openhour_wrap')
                    place_operation_time = []
                    
                    if len(operation_time) != 0:
                        time_operation_btn = detail_page_soup.select('.location_present > .list_operation > li > .btn_more')
                        
                        # 영업시간 더보기 버튼이 있을 시
                        if len(time_operation_btn) != 0:
                            driver.find_element_by_class_name("btn_more").send_keys(Keys.ENTER)
                            detail_page = driver.page_source
                            detail_page_soup = BeautifulSoup(detail_page, 'html.parser')
                            
                            operation_time_list = detail_page_soup.find("div", "inner_floor")
            
                            for elem in operation_time_list:
                                if elem.text == "\n" or "닫기" in elem.text:
                                    continue
                                for inner in elem:
                                    if inner.text == "\n":
                                        continue
                                    splitted_txt = ' '.join(inner.text.split())
                                    place_operation_time.append(splitted_txt)
                        # 영업시간 더보기 버튼이 없을 시
                        else:
                            # operation_time_list = detail_page_soup.select('.openhour_wrap > .location_present > .list_operation')
                            operation_time_list = detail_page_soup.select('.openhour_wrap > .location_present')
                            if len(operation_time_list) != 0:
                                for elem in operation_time_list:
                                    splitted_txt = elem.text.replace("영업중", "").replace("금일영업마감", "")
                                    splitted_txt = ' '.join(splitted_txt.split())
                                    place_operation_time.append(splitted_txt)
                    
                    # 홈페이지
                    place_homepage = detail_page_soup.select('.placeinfo_homepage > .location_detail > .location_present > a')
                    place_homepage = place_homepage[0].attrs.get("href") if len(place_homepage) != 0 else np.nan
                    
                    # 대표번호
                    place_tel = detail_page_soup.select('.placeinfo_contact > .location_detail > .location_present > .num_contact > .txt_contact')
                    place_tel = place_tel[0].text if len(place_tel) != 0 else np.nan
                    
                    # 태그
                    place_tags = detail_page_soup.select('.placeinfo_default > .location_detail > .txt_tag > .tag_g > a')
                    place_tags = [i.text for i in place_tags] if len(place_tags) != 0 else np.nan
                    
                    # 예약, 포장, 배달
                    place_etc = ""
                    if detail_page_soup.find("span", "ico_delivery") is not None:
                        place_etc = detail_page_soup.find("span", "ico_delivery").parent.parent
                        place_etc = place_etc.select('.location_detail')[0].text
                    
                    # 시설
                    place_facility = []
                    facilities = detail_page_soup.select(".placeinfo_facility")
                    
                    if len(facilities) != 0:
                        facilities = detail_page_soup.select(".placeinfo_facility > .list_facility > li")
                        for li in facilities:
                            place_facility.append(li.text.replace("\n", ""))    
                    
                    # 리뷰 수
                    total_evaluation = detail_page_soup.select('.total_evaluation > span')
                    total_evaluation = total_evaluation[0].text if len(total_evaluation) != 0 else np.nan
                    
                    # 평균 평점
                    average_rate = detail_page_soup.select('.grade_star > em')
                    average_rate = average_rate[0].text if len(average_rate) != 0 else np.nan

                    place_df = place_df.append({'name': place_name, 
                                                'category': place_category,
                                                'address': place_address, 
                                                'operation_time': place_operation_time,
                                                'homepage': place_homepage, 
                                                'tel': place_tel,
                                                'tag': place_tags, 
                                                'etc': place_etc,
                                                'facility': place_facility,
                                                'num_of_comments': total_evaluation, 
                                                'avg_rate': average_rate, 
                                                'url': driver.current_url},
                                                ignore_index=True)
                    
                    comments = detail_page_soup.select('.list_evaluation > li')
                    
                    # 후기 전체를 보기 위해 '후기 더보기' 클릭
                    if len(detail_page_soup.select('.evaluation_review > .link_more')) != 0:
                        # more_comment_button = driver.find_element_by_class_name('link_more')
                        # '후기 더보기" 버튼
                        more_comment_button = driver.find_element_by_xpath('//*[@class="evaluation_review"]/a')
                        button_classes = more_comment_button.get_attribute("class")
                        
                        # 댓글 내용이 길 때의 '더보기' 버튼
                        btn = driver.find_elements_by_xpath('//button[@class="btn_fold" and text()="더보기"]')

                        for b in btn:
                            if b.is_displayed():
                                b.click()
                        
                        # '후기 더보기' 버튼이 없어질 때까지 클릭
                        while "link_unfold" not in button_classes:
                            more_comment_button.send_keys(Keys.ENTER)
                            sleep(0.7)
                            
                            btn = driver.find_elements_by_xpath('//button[@class="btn_fold" and text()="더보기"]')

                            for b in btn:
                                if b.is_displayed():
                                    b.click()
                            # more_comment_button = driver.find_element_by_class_name('link_more')
                            more_comment_button = driver.find_element_by_xpath('//*[@class="evaluation_review"]/a')
                            button_classes = more_comment_button.get_attribute("class")
                    
                    
                    btn = driver.find_elements_by_xpath('//button[@class="btn_fold" and text()="더보기"]')

                    for b in btn:
                        if b.is_displayed():
                            b.click()
                    
                    if len(comments) != 0:
                        detail_page = driver.page_source
                        detail_page_soup = BeautifulSoup(detail_page, 'html.parser')
                        comments = detail_page_soup.select('.list_evaluation > li')
                        for i, comment in enumerate(comments):
                            txt_desc = comment.select('.txt_desc')
                            nickname = comment.select('.link_user')[0].text
                            total_comment = txt_desc[0].text
                            avg_rating = txt_desc[1].text
                            created_at = comment.select('.time_write')[0].text
                            rating = int(comment.select('.inner_star')[0]['style'][6:-2]) / 20
                            comment_txt = comment.select('.comment_info > .txt_comment > span')[0].text

                            comment_df = comment_df.append({'place_name': place_name, 
                                                            'nickname': nickname, 
                                                            'total_comments': total_comment, 
                                                            'avg_rating': avg_rating, 
                                                            'rating': rating, 
                                                            'comment': comment_txt, 
                                                            'created_at': created_at},
                                                            ignore_index=True)
                    
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    sleep(1)
                    
                scraped_page += 1
                print(str(scraped_page) + "페이지 스크랩 완료")
            
            # 검색결과 다음 페이지 버튼
            # class에 disabled 있는 경우 마지막 검색결과
            next_page_btn = driver.find_element_by_xpath('//*[@id="info.search.page.next"]')
            if "disabled" in next_page_btn.get_attribute("class"):
                break
            else:
                next_page_btn.send_keys(Keys.ENTER)
            
    driver.close()
    
    print(len(place_df))
    print(place_df)
    
    print(len(comment_df))
    print(comment_df)  
    
    now = datetime.now()
    now = now.strftime("%Y%m%d")
    
    place_df.to_csv(now + "_place.csv", na_rep="NaN", encoding="utf-8-sig")
    comment_df.to_csv(now + "_comment.csv", na_rep="NaN", encoding="utf-8-sig")
    # place_df.to_csv('place_info.csv', na_rep="NaN", encoding="utf-8-sig")
    # comment_df.to_csv('comment_info.csv', na_rep="NaN", encoding="utf-8-sig")
            
def main():
    scrap_from_kakaomap()
    
if __name__ == "__main__":
    main()