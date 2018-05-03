"""
Calls for Youtube API.
"""
import httplib2

# Google api libs
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials


def videos_list(user):
    """Return videos list of the MiwoUser"""
    # Search user's videos
    access_token = user.socialaccount_set.filter(provider="google")[0].socialtoken_set.first().token
    # TODO: manage refresh token
    credentials = AccessTokenCredentials(access_token, "Miwo")
    http = credentials.authorize(httplib2.Http())
    service = build("youtube", "v3", http)
    request = service.search().list(part="snippet", forMine="true", type="video", order="date", maxResults=15)
    response = request.execute()
    videos = []
    for video in response["items"]:
        videos.append(
            {"id": video["id"]["videoId"], "thumbnail_url": video["snippet"]["thumbnails"]["default"]["url"]}
        )
    return videos
