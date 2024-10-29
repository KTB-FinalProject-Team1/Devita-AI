# 베이스 이미지 설정 (Python 3.10 사용 예시)
FROM python:3.11-slim

# 작업 디렉토리 생성
WORKDIR /app

# poetry 설치
RUN pip install poetry

# poetry 버전 잠금을 해제하는 설정 (필요시)
RUN poetry config virtualenvs.create false

# 프로젝트 파일 복사
COPY pyproject.toml poetry.lock /app/

# 의존성 설치
RUN poetry install --no-root

# 소스 코드 복사
COPY . /app

# 실행할 명령어 설정
CMD ["poetry", "run", "python", "main.py"]
