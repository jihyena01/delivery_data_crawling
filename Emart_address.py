from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def load_all_addresses(driver):
    while True:
        try:
            more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "more_btn"))
            )
            more_button.click()
            time.sleep(2)  # 페이지 로딩을 기다립니다.
        except:
            break  # 더보기 버튼이 없으면 종료합니다.

def save_address_list(postcode):
    # Selenium WebDriver 설정
    driver_path = '/home/comet/chromedriver-linux64/chromedriver'  # chromedriver 경로를 설정하세요
    service = Service(driver_path)

    # Headless 모드 옵션 설정
    options = Options()
    options.headless = True  # headless 모드 설정 (True로 변경 가능)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Emart 웹사이트 열기
        driver.get('https://member.ssg.com/m/addr/zipcdShppInfo.ssg')

        # (1) postcode 입력란에 postcode 입력
        postcode_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "searchKeyword"))
        )
        postcode_input.click()
        postcode_input.clear()
        postcode_input.send_keys(postcode)
        
        # 검색 버튼 클릭
        search_button = driver.find_element(By.CLASS_NAME, 'search_btn')
        search_button.click()
        time.sleep(2)

        # (2) 더보기 버튼을 끝까지 눌러 모든 주소 로드
        load_all_addresses(driver)

        # (3) 모든 주소 리스트에서 주소 추출
        addresses = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".result_list li"))
        )

        address_data = {"도로명 주소": [], "지번 주소": []}
        for address_element in addresses:
            try:
                # 첫 번째 info_cont 요소에서 도로명 주소 추출
                road_address_text = address_element.find_element(By.CSS_SELECTOR, ".info_cont:nth-of-type(1)").text
                address_data["도로명 주소"].append(road_address_text)

                # 두 번째 info_cont 요소에서 지번 주소 추출
                jibun_address_text = address_element.find_element(By.CSS_SELECTOR, ".info_cont:nth-of-type(2)").text
                address_data["지번 주소"].append(jibun_address_text)
                
                # address_list.append({"도로명 주소": road_address_text, "지번 주소": jibun_address_text})

            except Exception as e:
                print(f"주소 추출 오류: {e}")

        # 주소 리스트를 DataFrame으로 변환하여 CSV 파일로 저장
        df = pd.DataFrame({"도로명 주소": address_data["도로명 주소"], "지번 주소": address_data["지번 주소"]})
        # df.to_csv(f"addresses_{postcode}.csv", index=False)
        df.to_csv(f"addresses_{postcode}.csv", index=False)
        
    finally:
        # 브라우저 닫기
        driver.quit()

# 실행 예시
postcode = "경기도 부천시 소사구 송내동 303-5"  # 원하는 우편번호 입력
save_address_list(postcode)
