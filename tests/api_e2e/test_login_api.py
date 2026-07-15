import pytest
from playwright.sync_api import APIRequestContext

from api import login_api


def test_signup_and_login_response(request_context: APIRequestContext, account_data):
    """
    LOGIN-API-TS-001: 정상 회원가입/로그인 응답 검증
    Precondition: 신규 계정 생성
    """
    # 1. POST /api/createAccount 로 신규 계정 생성
    create_body = login_api.create_account(request_context, **account_data).json()
    assert create_body["responseCode"] == 201
    assert create_body["message"] == "User created!"

    # 2. POST /api/verifyLogin 으로 로그인 검증
    login_body = login_api.verify_login(
        request_context, account_data["email"], account_data["password"]
    ).json()
    assert login_body["responseCode"] == 200
    assert login_body["message"] == "User exists!"

    # 3. GET /api/getUserDetailByEmail 로 등록정보 조회 > 가입 시 입력값과 일치 검증
    detail_body = login_api.get_user_detail_by_email(request_context, account_data["email"]).json()
    assert detail_body["responseCode"] == 200
    user = detail_body["user"]
    assert user["email"] == account_data["email"]
    assert user["name"] == account_data["name"]
    assert user["title"] == account_data["title"]
    assert user["first_name"] == account_data["firstname"]
    assert user["last_name"] == account_data["lastname"]
    assert user["company"] == account_data["company"]
    assert user["address1"] == account_data["address1"]
    assert user["country"] == account_data["country"]
    assert user["state"] == account_data["state"]
    assert user["city"] == account_data["city"]
    assert user["zipcode"] == account_data["zipcode"]

@pytest.mark.smoke
def test_update_account_response(request_context: APIRequestContext, account_data):
    """
    LOGIN-API-TS-002: 계정 정보 변경에 따른 응답 검증
    """
    assert login_api.create_account(request_context, **account_data).json()["responseCode"] == 201

    old_password = account_data["password"]
    new_password = "NewTest5678!"

    # 1. PUT /api/updateAccount 로 비밀번호 변경
    updated_payload = dict(account_data, password=new_password)
    update_body = login_api.update_account(request_context, **updated_payload).json()
    assert update_body["responseCode"] == 200
    assert update_body["message"] == "User updated!"

    # 이후 로그인 검증 및 fixture 정리 단계에서 신규 비밀번호를 사용하도록 갱신
    account_data["password"] = new_password

    # 2. POST /api/verifyLogin 으로 구 비밀번호 로그인 시도
    old_login_body = login_api.verify_login(request_context, account_data["email"], old_password).json()
    assert old_login_body["responseCode"] == 404
    assert old_login_body["message"] == "User not found!"

    # 3. POST /api/verifyLogin 으로 변경한 신규 비밀번호 로그인 시도
    new_login_body = login_api.verify_login(
        request_context, account_data["email"], new_password
    ).json()
    assert new_login_body["responseCode"] == 200
    assert new_login_body["message"] == "User exists!"


def test_delete_account_response(request_context: APIRequestContext, account_data):
    """
    LOGIN-API-TS-003: 계정 삭제 응답 검증
    """
    assert login_api.create_account(request_context, **account_data).json()["responseCode"] == 201

    # 1. POST /api/verifyLogin 으로 삭제 전 로그인 가능 상태 확인
    before_body = login_api.verify_login(
        request_context, account_data["email"], account_data["password"]
    ).json()
    assert before_body["responseCode"] == 200
    assert before_body["message"] == "User exists!"

    # 2. DELETE /api/deleteAccount 로 계정 삭제
    delete_body = login_api.delete_account(
        request_context, account_data["email"], account_data["password"]
    ).json()
    assert delete_body["responseCode"] == 200
    assert delete_body["message"] == "Account deleted!"

    # 3. POST /api/verifyLogin 으로 삭제한 계정 재로그인 시도
    after_body = login_api.verify_login(
        request_context, account_data["email"], account_data["password"]
    ).json()
    assert after_body["responseCode"] == 404
    assert after_body["message"] == "User not found!"
