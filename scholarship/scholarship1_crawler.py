from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_scholarships(limit=30):
    """
    장학금 정보를 크롤링하는 함수.
    - 최대 크롤링 항목: limit
    """
    # URL 설정
    url = "https://onestop.pusan.ac.kr/page?menuCD=000000000000062#popup"
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # "20개씩 보기" 옵션 선택
        select = Select(WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "pageSel"))
        ))
        select.select_by_value("20")

        # 테이블 데이터 로드 대기
        WebDriverWait(driver, 20).until(
            lambda d: len(d.find_elements(By.TAG_NAME, "tr")) >= 15
        )

        results = []
        links = driver.find_elements(By.CSS_SELECTOR, "td.text-left a")

        count = 0
        for index, link in enumerate(links):
            # 제한된 개수 초과 시 중단
            if count >= limit:
                break
            # 첫 5개의 링크는 건너뜀
            if index < 5:
                continue

            link_text = link.text.strip()
            link.click()

            # 링크 클릭 후 페이지 로드 대기
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # 현재 URL 추출
            current_url = driver.current_url
            results.append({"name": link_text, "link": current_url, "page_id": 0})
            count += 1

            # 뒤로가기
            driver.back()

            # 뒤로가기 후 링크 다시 로드
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.text-left a"))
            )
            links = driver.find_elements(By.CSS_SELECTOR, "td.text-left a")

        return results

    except Exception as e:
        print(f"오류 발생: {e}")
        return []

    finally:
        driver.quit()