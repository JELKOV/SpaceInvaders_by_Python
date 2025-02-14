# Python 최신 버전 사용
FROM python:3.13

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 게임 소스 복사
COPY src /app/src
COPY data /app/data
COPY assets /app/assets  # 사운드, 이미지 포함

# 실행
CMD ["python", "src/main.py"]