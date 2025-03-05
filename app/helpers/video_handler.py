from googleapiclient.discovery import build

from app.core.config import settings

API_KEY = settings.API_KEY
def get_youtube_info_api(video_url):
    try:
        video_id = video_url.split("v=")[1].split("&")[0]
        youtube = build("youtube", "v3", developerKey=API_KEY)
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()

        if "items" in response and response["items"]:
            snippet = response["items"][0]["snippet"]
            return {
                "title": snippet["title"],
                "description": snippet["description"]
            }
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

