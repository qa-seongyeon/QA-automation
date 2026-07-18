import allure
from playwright.sync_api import Page


def attach_screenshot(page: Page, name: str = "failure_screenshot"):
    """
    실패 시점의 페이지 스크린샷을 Allure 리포트에 첨부.
    페이지가 이미 닫혔거나 크래시한 경우 원래 실패 원인이 가려지지 않도록 조용히 무시.
    """
    try:
        screenshot_bytes = page.screenshot()
    except Exception:
        return

    allure.attach(
        screenshot_bytes,
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )
