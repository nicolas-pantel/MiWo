import urbanairship as ua

from django.conf import settings

from backoffice import models


def publish(user):
    """Send notifaction to followers on publication"""
    followers = user.followers.all()
    for follower in followers:
        airship = ua.Airship(settings.URBANAIRSHIP_KEY, settings.URBANAIRSHIP_MASTER_SECRET)
        push = airship.create_push()
        push.notification = ua.notification(
            ios=ua.ios(
                alert="New publication from {}".format(user.username),
                badge='+1',
            )
        )
        push.device_types = ua.device_types('ios')
        devices = models.Device.objects.filter(profile=follower.profile)
        if devices.exists():
            device = devices[0]
            push.audience = ua.ios_channel(device.chanid)
            push.send()
