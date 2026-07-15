import pytest
from playwright.sync_api import Page, expect
from config import settings
from pageobject.login_page import LoginPage

MAIN_URL = f"{settings.BASE_URL}/"
LOGIN_URL = f"{settings.BASE_URL}/login"
CART_URL = f"{settings.BASE_URL}/view_cart"
ADD_TO_CART_URL = f"{settings.BASE_URL}/add_to_cart/1"

@pytest.mark.smoke
def test_login_from_main_page(page: Page):
    """
    TS-LOGIN-001: 메인페이지 → 로그인 → 메인페이지 여정 검증
    """
    login_page = LoginPage(page)
    page.goto(MAIN_URL)

    # 1. 메인페이지 > 로그인 선택
    page.get_by_role("link", name="Signup / Login").click()
    expect(page).to_have_url(LOGIN_URL)

    # 2. 로그인 성공 시 메인페이지 이동
    # 3. 메인 페이지 상태 메뉴 > 아이디 노출
    login_page.login(settings.TEST_EMAIL_VALID, settings.TEST_PASSWORD_VALID)
    login_page.assert_login_success(settings.TEST_USERNAME)


def test_login_from_cart_page(page: Page):
    """
    TS-LOGIN-002: 장바구니 → 로그인 → 메인페이지 여정 검증
    """
    login_page = LoginPage(page)

    # Precondition: 장바구니 아이템 존재
    # NOTE: automationexercise.com은 장바구니 관련 공개 API가 없어,
    # 브라우저 세션 쿠키를 공유하는 page.request.get()으로 내부 add_to_cart 엔드포인트를 직접 호출함.
    # 문서화되지 않은 구현이라 응답 200이 실제 상품 담김을 보장하지 않으므로,
    # 아래에서 장바구니 화면의 상품 행을 통해 담김 여부를 다시 확인하는 방식으로 보완.
    response = page.request.get(ADD_TO_CART_URL)
    assert response.ok

    page.goto(CART_URL)
    expect(page.locator("#cart_info_table tbody tr")).to_have_count(1)

    # 1. 장바구니 > 구매하기 선택
    page.locator(".check_out").click()

    # 2. 로그인 팝업 > 로그인 화면 이동
    page.locator("#checkoutModal").get_by_role("link", name="Register / Login").click()
    expect(page).to_have_url(LOGIN_URL)

    # 3. 로그인 성공 시 메인페이지 이동
    # 4. 메인 페이지 상태 메뉴 > 아이디 노출
    login_page.login(settings.TEST_EMAIL_VALID, settings.TEST_PASSWORD_VALID)
    login_page.assert_login_success(settings.TEST_USERNAME)
