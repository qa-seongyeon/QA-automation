import re
import uuid
import pytest
from playwright.sync_api import Playwright

from api import login_api
from utils.allure_utils import attach_screenshot
from utils.data_utils import build_account_payload

AD_PATTERN = re.compile(r"(doubleclick|googlesyndication|google_vignette|adservice\.google)")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실패 시(call 단계 한정) page fixture가 있으면 스크린샷을 Allure에 첨부.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            attach_screenshot(page, name=f"failure_{item.name}")


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


@pytest.fixture
def account_data(request_context):
    """테스트마다 고유한 이메일의 신규 계정 데이터 생성 (테스트 종료 후 잔여 계정 정리)"""
    unique = uuid.uuid4().hex[:12]
    data = build_account_payload(email=f"qa_{unique}@example.com", password="Test1234!")
    yield data
    login_api.delete_account(request_context, data["email"], data["password"])
