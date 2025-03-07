from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.helpers.paging import PaginationParams
from app.models import Video
from tests.providers import CommonProvider

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


def test_get_videos(client: TestClient,  db_session: Session):
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
