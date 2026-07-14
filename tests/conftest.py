import re
import uuid
import pytest
from playwright.sync_api import Playwright

from api import login_api

AD_PATTERN = re.compile(r"(doubleclick|googlesyndication|google_vignette|adservice\.google)")


@pytest.fixture
def page(context):
    page = context.new_page()
    page.route(AD_PATTERN, lambda route: route.abort())
    yield page
    page.close()


@pytest.fixture
def request_context(playwright: Playwright):
    request_context = playwright.request.new_context()
    yield request_context
    request_context.dispose()


def build_account_payload(email: str, password: str) -> dict:
    """createAccount/updateAccount API가 요구하는 공통 계정 payload"""
    return {
        "name": "QA Tester",
        "email": email,
        "password": password,
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "1",
        "birth_year": "1990",
        "firstname": "QA",
        "lastname": "Tester",
        "company": "QA Corp",
        "address1": "123 Test St",
        "address2": "",
        "country": "United States",
        "zipcode": "12345",
        "state": "California",
        "city": "Los Angeles",
        "mobile_number": "01000000000",
    }


@pytest.fixture
def account_data(request_context):
    """테스트마다 고유한 이메일의 신규 계정 데이터 생성 (테스트 종료 후 잔여 계정 정리)"""
    unique = uuid.uuid4().hex[:12]
    data = build_account_payload(email=f"qa_{unique}@example.com", password="Test1234!")
    yield data
    login_api.delete_account(request_context, data["email"], data["password"])
