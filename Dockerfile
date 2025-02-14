# 베이스 이미지 설정
FROM python:3.13

# 작업 디렉토리 설정
WORKDIR /app

# ✅ PYTHONPATH 설정 (src 폴더를 인식할 수 있도록 추가)
ENV PYTHONPATH="/app"
# Docker에서 실행할 때 사운드 기능을 비활성화하기 위한 환경변수 설정
ENV RUNNING_IN_DOCKER=true

# 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 및 데이터 복사
COPY src /app/src
COPY data /app/data
COPY assets /app/assets

# 실행
CMD ["python", "src/main.py"]