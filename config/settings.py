import os
from dotenv import load_dotenv

load_dotenv()

# 환경 구분 (staging/prod)
ENV = os.environ.get("TEST_ENV", "prod")

if ENV == "staging":
    BASE_URL = "https://staging.automationexercise.com"  # 스테이징 주소
else:
    BASE_URL = "https://automationexercise.com"          # 운영 주소

API_BASE_URL = f"{BASE_URL}/api"

# 테스트 계정 정보 (.env 파일에서 로드)
TEST_EMAIL = os.environ.get("TEST_EMAIL", "changeme@example.com")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "changeme")

