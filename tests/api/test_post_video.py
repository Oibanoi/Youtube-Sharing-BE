import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.helpers.login_manager import login_required
from app.main import app  # Import the FastAPI app from your project
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

def test_create_video(client,bypass_auth):
    # Mock data for the new video creation
    video_data = {
        "video_url": "https://youtube.com/new_video"
    }


    response = client.post("/videos", json=video_data)  # Replace with your actual path

    print(response.json())
        # Check the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["code"] == "000"
    assert response_data["data"]["title"] == "title"
    assert response_data["data"]["description"] == "description"
    assert response_data["data"]["youtubeUrl"] == "https://youtube.com/new_video"

