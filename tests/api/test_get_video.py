import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from app.models import User, Video
from app.schemas.sche_video import VideoItemResponse
from app.helpers.paging import paginate, PaginationParams, Page
from app.schemas.sche_base import MetadataSchema
from tests.providers import CommonProvider

# Mock user data for bypassing authentication
mock_user = User(id=1, email="user@example.com")

# Mock video data to simulate the response from the paginate function
mock_video_data = [
    VideoItemResponse(id=1, title="Video 1", description="Description 1", user_name="user1@example.com",
                      youtube_url="https://youtube.com/video1"),
    VideoItemResponse(id=2, title="Video 2", description="Description 2", user_name="user2@example.com",
                      youtube_url="https://youtube.com/video2")
]
def init_data(session:Session):
    videos=[
        Video(
            id=1,
            title="Video 1",
            description="Description 1",
            youtube_url="https://youtube.com/video1",
            user_id=1
        ),
        Video(
            id=2,
            title="Video 2",
            description="Description 2",
            youtube_url="https://youtube.com/video2",
            user_id=1
        )
    ]
    return CommonProvider.create(session=session,models=videos)


def test_get_videos(client,  db_session: Session):
    # Mock pagination parameters
    params = PaginationParams(page=1, page_size=2, order="asc", sort_by="title")
    data=init_data(db_session)
    # Call the API endpoint with the mocked paginate function
    response = client.get("/videos", params={"page": params.page, "page_size": params.page_size})

    # Assert the response is correct
    assert response.status_code == 200
    data = response.json()
    print(data)
    # Ensure the data matches the mock response
    assert len(data["data"]) == 2  # We mocked 2 videos
    assert data["data"][0]["title"] == "Video 1"
    assert data["data"][1]["user_name"] == "user2@example.com"

    # Ensure metadata is included in the response
    assert "metadata" in data
    assert data["metadata"]["current_page"] == 1
    assert data["metadata"]["total_items"] == 10  # Mocked total items count
