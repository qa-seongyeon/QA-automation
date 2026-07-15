from playwright.sync_api import APIRequestContext, APIResponse

from config.settings import API_BASE_URL

#
# API 호출 로직을 함수 단위로 설계하여
# 앤드포인트/인증 방식 변경 시 해당 함수만 수정하면 되도록 tests/api_e2e 와 분리
#

def create_account(request_context: APIRequestContext, **account_data) -> APIResponse:
    """POST /createAccount - 회원가입"""
    return request_context.post(f"{API_BASE_URL}/createAccount", form=account_data)


def verify_login(request_context: APIRequestContext, email: str, password: str) -> APIResponse:
    """POST /verifyLogin - 로그인 가능 여부 확인"""
    return request_context.post(
        f"{API_BASE_URL}/verifyLogin", form={"email": email, "password": password}
    )


def get_user_detail_by_email(request_context: APIRequestContext, email: str) -> APIResponse:
    """GET /getUserDetailByEmail - 이메일로 가입정보 조회"""
    return request_context.get(f"{API_BASE_URL}/getUserDetailByEmail", params={"email": email})


def update_account(request_context: APIRequestContext, **account_data) -> APIResponse:
    """PUT /updateAccount - 가입정보 수정"""
    return request_context.put(f"{API_BASE_URL}/updateAccount", form=account_data)


def delete_account(request_context: APIRequestContext, email: str, password: str) -> APIResponse:
    """DELETE /deleteAccount - 회원 탈퇴"""
    return request_context.delete(
        f"{API_BASE_URL}/deleteAccount", form={"email": email, "password": password}
    )
