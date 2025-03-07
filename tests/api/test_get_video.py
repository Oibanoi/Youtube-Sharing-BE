from fastapi.testclient import TestClient
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.helpers.paging import PaginationParams
from app.models import User
from tests.faker import fake


def test_get_videos(client: TestClient,  db_session: Session):
    params = PaginationParams(page=1, page_size=2, order="asc", sort_by="title")
    current_user: User = fake.user({'password': 'secret123'})
    video1= fake.video({
        "title" : "Video 1",
    "description" : "Description 1",
    "youtube_url" : "https://youtube.com/video1",
    "user_id" : 1
    })
    video2 = fake.video({
        "title": "Video 2",
        "description": "Description 2",
        "youtube_url": "https://youtube.com/video2",
        "user_id": 1
    })
    # Call the API endpoint with the mocked paginate function
    response = client.get("/videos", params={"page": params.page, "page_size": params.page_size})
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["data"][0]["title"] == "Video 1"
    assert data["data"][1]["description"] == "Description 2"

    # Ensure metadata is included in the response
    assert "metadata" in data
    assert data["metadata"]["current_page"] == 1
    assert data["metadata"]["total_items"] == 2