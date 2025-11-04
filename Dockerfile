FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# 포트 노출
EXPOSE 5000

# 환경 변수 설정 (선택사항)
# ENV SUBFOLDER=/api

# 애플리케이션 실행
CMD ["python", "app.py"]

