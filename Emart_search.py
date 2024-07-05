from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def check_emart_delivery(postcode):
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

        # (2) 제일 먼저 나오는 주소 클릭
        first_address = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "result_list"))
        )
        first_address.click()
        time.sleep(2)


        # (3) 배송 가능 여부 확인 (예제 HTML 코드 기반으로 가정)
        try:
            shpp_area = driver.find_element(By.ID, "shppArea")
            non_shpp_area = driver.find_element(By.ID, "nonShppArea")

            if shpp_area.is_displayed() and not non_shpp_area.is_displayed():
                return "배송 가능합니다."
            else:
                return "배송 불가능합니다."
        except Exception as e:
            print(f"Error checking delivery status: {e}")
            return "배송 불가능합니다."
    finally:
        # 브라우저 닫기
        driver.quit()

def main(postcodes):
    result = []
    for postcode in postcodes:
        status = check_emart_delivery(postcode)
        result.append({"주소": postcode, "배송 가능 여부": status})
    df = pd.DataFrame(result)
    df.to_csv('emart_delivery_status.csv', index=False)
    print(df)
        

# CSV 파일 불러오기
postcodes = pd.read_csv('addresses_경기도 부천시 소사구 송내동 303-5.csv')
# print(address)
main(postcodes['지번 주소'])

