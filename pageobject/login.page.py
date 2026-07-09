from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        
        #로그인 페이지 > 로그인 요소 정의
        self.login_email = page.locator('[data-qa="login-email"]') 
        self.login_password = page.locator('[data-qa="login-password"]')
        self.login_btn = page.locator('[data-qa="login-button"]')

        #로그인 페이지 > 회원가입 요소 정의
        self.signup_name = page.locator('[data-qa="signup-name"]')
        self.signup_email = page.locator('[data-qa="signup-email"]')
        self.signup_btn = page.locator('[data-qa="signup-button"]')

        #로그인 페이지 > 로그인 실패 에러메세지 정의
        self.login_error_msg = page.get_by_text('Your email or password is incorrect!')

        #로그인 페이지 > 회원가입 중복 이메일 에러메세지 정의
        self.signup_error_msg = page.get_by_text('Email Address already exist!')
