# 공식 Python 이미지를 사용합니다.
FROM python:3.12-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 종속성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Selenium 사용을 위한 Chrome 및 ChromeDriver 설치
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && \
    apt-get update && apt-get install -y ./chrome.deb && rm -rf ./chrome.deb && \
    curl -sSL https://chromedriver.storage.googleapis.com/116.0.5845.96/chromedriver_linux64.zip -o chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver.zip

# Python 패키지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# FastAPI 포트 노출
EXPOSE 8000

# FastAPI 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
