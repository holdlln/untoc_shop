from bs4 import BeautifulSoup
from selenium import webdriver
import time
from urllib.parse import urljoin

def fetch_scholarships2(limit=15):
    """
    Selenium과 BeautifulSoup을 사용해 장학금 데이터를 크롤링하는 함수.

    Parameters:
    - limit: 최대 크롤링할 항목 수 (기본값: 15)

    Returns:
    - List[dict]: 크롤링한 장학금 데이터 리스트
    """
    url = "https://cse.pusan.ac.kr/cse/14651/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGY3NlJTJGMjYwNSUyRmFydGNsTGlzdC5kbyUzRmJic09wZW5XcmRTZXElM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjZzcmNoQ29sdW1uJTNEc2olMjZwYWdlJTNEMSUyNnNyY2hXcmQlM0QlMjZyZ3NCZ25kZVN0ciUzRCUyNmJic0NsU2VxJTNENDIyOSUyNnJnc0VuZGRlU3RyJTNEJTI22"
    driver = webdriver.Chrome()
    driver.get(url)

    # 페이지 로드 대기
    time.sleep(5)

    # HTML 가져오기
    html = driver.page_source
    driver.quit()

    # BeautifulSoup로 HTML 파싱
    soup = BeautifulSoup(html, "lxml")

    # 데이터 저장용 리스트
    results = []

    # 데이터 추출
    elements = soup.select("td._artclTdTitle")  # `td._artclTdTitle` 선택
    count = 0
    for element in elements:
        if count >= limit:  # 최대 크롤링 항목 제한
            break

        a_tag = element.find("a")  # <a> 태그 찾기
        if a_tag:  # <a> 태그가 있는 경우
            strong_tag = a_tag.find("strong")  # <strong> 태그 찾기
            if strong_tag:  # <strong> 태그가 있는 경우
                text = strong_tag.get_text(strip=True)  # 텍스트 추출
                if text.startswith("[장학]"):  # "[장학]"으로 시작하는 경우만 저장
                    link = urljoin(url, a_tag.get("href"))  # 링크 URL 절대 경로 변환
                    results.append({"name": text, "link": link, "page_id": 2})
                    count += 1

    return results
