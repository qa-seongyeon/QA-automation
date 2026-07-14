import pytest
from playwright.sync_api import Page, expect
from config import settings
from pageobject.login_page import LoginPage

LOGIN_URL = f"{settings.BASE_URL}/login"

# 로그인 실패 테스트 (TC 시트 LOGIN-TC-001 ~ 007)
# (email, password, validation_type, invalid_field, validity_state)
#
# validation_type "server" -> 서버가 에러 메시지로 응답하는 케이스 (TC-001, TC-002)
# validation_type "client" -> 브라우저 검증으로 서버 요청 자체가 안 나가는 케이스 (TC-003~007)
# validity_state           -> TC 시트 Comment 컬럼의 "validity state"와 1:1 매칭
#                              (valueMissing: 필수값 공백 / typeMismatch: 이메일 형식 불일치)
LOGIN_FAILURE_CASES = [
    pytest.param(
        settings.TEST_EMAIL_VALID, settings.TEST_PASSWORD_INVALID,
        "server", None, None,
        id="LOGIN-TC-001_유효한이메일_잘못된비밀번호",
    ),
    pytest.param(
        settings.TEST_EMAIL_INVALID, settings.TEST_PASSWORD_INVALID,
        "server", None, None,
        id="LOGIN-TC-002_유효하지않는이메일_비밀번호",
    ),
    pytest.param(
        settings.TEST_EMAIL_VALID, "",
        "client", "password", "valueMissing",
        id="LOGIN-TC-003_이메일_비밀번호공백",
    ),
    pytest.param(
        "", "",
        "client", "email", "valueMissing",
        id="LOGIN-TC-004_이메일공백_비밀번호공백",
    ),
    pytest.param(
        "invalid-email-format", settings.TEST_PASSWORD_VALID,
        "client", "email", "typeMismatch",
        id="LOGIN-TC-005_이메일형식오류",
    ),
    # NOTE: 이메일 input의 type="email" 속성 때문에 SQL 인젝션 payload가
    # 서버로 가기도 전에 브라우저 typeMismatch로 먼저 차단됨(의도치 않은 방어).
    # 그래도 "보안 테스트 설계 의도"를 유지하기 위해 데이터는 그대로 남기고,
    # 실제 검증은 client(typeMismatch) 기준으로 처리.
    pytest.param(
        "test@gmail.com'OR'1'='1", settings.TEST_PASSWORD_VALID,
        "client", "email", "typeMismatch",
        id="LOGIN-TC-006_SQL인젝션",
    ),
    # NOTE: XSS payload도 위와 동일한 이유(이메일 type 검증)로 브라우저 단에서 차단됨
    pytest.param(
        "<script>alert(1)</script>@gmail.com", settings.TEST_PASSWORD_VALID,
        "client", "email", "typeMismatch",
        id="LOGIN-TC-007_XSS인젝션",
    ),
]


@pytest.mark.regression
@pytest.mark.parametrize(
    "email, password, validation_type, invalid_field, validity_state",
    LOGIN_FAILURE_CASES,
)
def test_login_failure(page: Page, email, password, validation_type, invalid_field, validity_state):
    """
    로그인 실패 시나리오 검증 (서버검증 / 브라우저검증)
    """
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    login_page.login(email, password)

    # 서버 검증 (TC-001, TC-002): 화면에 서버 에러 메시지가 노출되어야 함
    if validation_type == "server":
        expect(login_page.login_error_msg).to_be_visible()
        expect(page).to_have_url(LOGIN_URL)
        return

    # 브라우저검증 (TC-003~007): TC 시트에 명시된 validity state와 그대로 매칭
    target = login_page.login_email if invalid_field == "email" else login_page.login_password
    assert target.evaluate(f"el => el.validity.{validity_state}") is True
    assert target.evaluate("el => el.validity.valid") is False

    # 서버로 요청 자체가 안 나갔으므로 URL 유지 + 서버 에러 메시지는 없어야 함
    expect(page).to_have_url(LOGIN_URL)
    expect(login_page.login_error_msg).not_to_be_visible()


@pytest.mark.regression
def test_login_success(page: Page):
    """
    LOGIN-TC-008: 미로그인 상태에서 로그인 성공 시나리오 검증
    """
    login_page = LoginPage(page)
    page.goto(LOGIN_URL)
    login_page.login(settings.TEST_EMAIL_VALID, settings.TEST_PASSWORD_VALID)

    expect(page).to_have_url(f"{settings.BASE_URL}/")
    expect(page.get_by_text("Logged in as")).to_be_visible()