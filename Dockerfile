<<<<<<< HEAD
FROM python:3.11-slim

WORKDIR /app

# 기본 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt-get/lists/*

# 파이썬 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 파일 복사 및 업로드 폴더 생성
COPY . .
RUN mkdir -p uploads

EXPOSE 10000

# Render 기본 포트(10000)로 uvicorn 실행
=======
FROM python:3.11-slim

WORKDIR /app

# 기본 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt-get/lists/*

# 파이썬 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 파일 복사 및 업로드 폴더 생성
COPY . .
RUN mkdir -p uploads

EXPOSE 10000

# Render 기본 포트(10000)로 uvicorn 실행
>>>>>>> c5c0c91a70907bbcdfe357bfc95238f53a289969
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]