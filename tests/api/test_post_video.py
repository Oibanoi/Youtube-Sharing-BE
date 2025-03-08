import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.helpers.login_manager import login_required
from app.helpers.video_handler import get_youtube_info_api
from app.main import app
from app.models import User
from app.schemas.sche_video import VideoCreateRequest

@pytest.fixture
def client():
    return TestClient(app)

mock_user = User(id=1, email="user@example.com")

@pytest.fixture
def bypass_auth():
    app.dependency_overrides[login_required] = lambda: mock_user
    yield
    del app.dependency_overrides[login_required]

def test_create_video(client, bypass_auth):
    with patch('app.helpers.video_handler.get_youtube_info_api') as mock_get_youtube_info_api:
        mock_get_youtube_info_api.return_value = {
            "title": "Mock Title",
            "description": "Mock Description"
        }
        video_data = {
            "video_url": "https://www.youtube.com/watch?v=CL13X-8o4h0"
        }

        response = client.post("/videos", json=video_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["code"] == "000"
        assert response_data["data"]["title"] == "BẮC BLING (BẮC NINH) | OFFICIAL MV | HOÀ MINZY ft NS XUÂN HINH x MASEW x TUẤN CRY"
        assert response_data["data"]["youtubeUrl"] == "https://www.youtube.com/watch?v=CL13X-8o4h0"

def test_create_video_err_when_url_none(client, bypass_auth):
    video_data = {
        "video_url": ""
    }

    response = client.post("/videos", json=video_data)
    print(response.json())
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "URL is null"


def test_create_video_err_when_url_not_valid(client, bypass_auth):
    video_data = {
        "video_url": "afas"
    }

    response = client.post("/videos", json=video_data)
    print(response.json())
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Video not found"