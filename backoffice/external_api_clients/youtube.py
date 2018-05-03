"""
Calls for Youtube API.
"""
import httplib2

# Google api libs
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials


def service(user):
    access_token = user.socialaccount_set.filter(provider="google")[0].socialtoken_set.first().token
    # TODO: manage refresh token
    credentials = AccessTokenCredentials(access_token, "Miwo")
    http = credentials.authorize(httplib2.Http())
    service = build("youtube", "v3", http)
    return service


def videos_list(user):
    """Return videos list of the MiwoUser"""
    # Search user's videos
    request = service(user).search().list(part="snippet", forMine="true", type="video", order="date", maxResults=15)
    response = request.execute()
    videos = []
    for video in response["items"]:
        videos.append(
            {"id": video["id"]["videoId"], "thumbnail_url": video["snippet"]["thumbnails"]["default"]["url"]}
        )
    return videos


def video_details(user, video_id_list):
    """Return some details of a list of videos"""
    request = service(user).videos().list(part="snippet,status", id=",".join(video_id_list))
    response = request.execute()
    return [(
        item["id"],
        item["snippet"]["thumbnails"]["default"]["url"],
        item["status"]["privacyStatus"]
    ) for item in response["items"]]
