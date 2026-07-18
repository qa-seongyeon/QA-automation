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
