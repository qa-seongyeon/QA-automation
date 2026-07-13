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
TEST_EMAIL_VALID = os.environ.get("TEST_EMAIL_VALID", "changeme@example.com")
TEST_PASSWORD_VALID = os.environ.get("TEST_PASSWORD_VALID", "changeme")

# 로그인 실패 케이스 검증용 (미가입 이메일)
TEST_EMAIL_INVALID = os.environ.get("TEST_EMAIL_INVALID", "invalid@example.com")
TEST_PASSWORD_INVALID = os.environ.get("TEST_PASSWORD_INVALID", "changeme")

