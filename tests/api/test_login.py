from starlette.testclient import TestClient

from app.core.config import settings
from app.models import User
from tests.faker import fake


class TestLogin:
    def test_success(self, client: TestClient):
        """
            Test api user login success
            Step by step:
            - Khởi tạo data mẫu với password hash
            - Gọi API Login
            - Đầu ra mong muốn:
                . status code: 200
                . access_token != null
                . token_type == 'bearer'
        """
        current_user: User = fake.user({'password': 'secret123'})
        r = client.post(f"{settings.API_PREFIX}/login", json={
            'username': current_user.email,
            'password': 'secret123'
        })
        assert r.status_code == 200
        response = r.json()
        print(response)
        assert response['data']['accessToken'] is not None
        assert response['data']['tokenType'] == 'bearer'

    def test_incorrect_password(self, client: TestClient):
        """
            Test api user login with incorrect password
            Step by step:
            - Khởi tạo data mẫu với password hash
            - Gọi API Login với wrong password
            - Đầu ra mong muốn:
                . status code: 400
        """
        current_user: User = fake.user({'password': 'secret123'})
        r = client.post(f"{settings.API_PREFIX}/login", json={
            'username': current_user.email,
            'password': 'secret1234'
        })
        assert r.status_code == 400


