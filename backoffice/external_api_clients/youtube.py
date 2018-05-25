"""
Calls for Youtube API.
"""
import httplib2

# Google api libs
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials


def service(user):
    credentials = GoogleCredentials(
        access_token=user.socialaccount_set.get(provider="google").socialtoken_set.first().token,
        refresh_token=user.socialaccount_set.get(provider="google").socialtoken_set.first().token_secret,
        client_id=user.socialaccount_set.get(provider="google").socialtoken_set.first().app.client_id,
        client_secret=user.socialaccount_set.get(provider="google").socialtoken_set.first().app.secret,
        token_expiry=user.socialaccount_set.get(provider="google").socialtoken_set.first().expires_at,
        token_uri='https://accounts.google.com/o/oauth2/token',
        user_agent="Miwo",
    )
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
            {
                "id": video["id"]["videoId"],
                "thumbnail_url": video["snippet"]["thumbnails"]["default"]["url"],
                "name": video["snippet"]["title"]
            }
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


def video_status(user, video_id):
    """Limited credit cost for video status only"""
    request = service(user).videos().list(part="status", id=video_id)
    response = request.execute()
    return response["items"][0]["status"]["privacyStatus"]


def videos_status(user, video_id_list):
    """Limited credit cost for a list of video status only"""
    request = service(user).videos().list(part="id,status", id=",".join(video_id_list))
    response = request.execute()
    return [(
        item["id"],
        item["status"]["privacyStatus"]
    ) for item in response["items"]]


def set_video_privacy(user, video_id, privacy):
    """
    Set video privacy status
    :param user: MiWo user
    :param video_id: YT video id
    :param privacy: 'private' or 'public'
    :return: None
    """
    request = service(user).videos().update(
        body={'id': video_id, 'status': {'privacyStatus': privacy, 'embeddable': True}},
        part='status')
    request.execute()
