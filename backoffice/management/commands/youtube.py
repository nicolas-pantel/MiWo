from django.core.management.base import BaseCommand

from backoffice import models
from backoffice.external_api_clients import youtube, urbanairship


class Command(BaseCommand):
    help = 'Query Youtube API for private videos status'

    def handle(self, *args, **options):
        print("youtube management command")
        # For each influencer
        influencers = models.MiwoUser.objects.filter(campaigns__isnull=False).distinct()
        for influencer in influencers:
            # Query YT for influencer's private videos
            if influencer.socialaccount_set.filter(provider="google"):
                publications = models.Publication.objects.filter(campaign__user=influencer, published=False)
                videos_ids = [publication.get_youtube_video_id() for publication in publications]
                status = youtube.videos_status(influencer, videos_ids)
                status = set(status)
                # Change status from public to private
                changed_videos = [statut for statut in status if statut[1] == "public"]
                print(changed_videos)
                for changed_video in changed_videos:
                    publications = models.Publication.objects.filter(video_id=changed_video[0])
                    print("UPDATE")
                    publications.update(published=True)
                    # Push notification to followers
                    # TODO: use async for scale
                    print(publications)
                    for publication in publications:
                        print("BEFORE PUSH")
                        urbanairship.publish(influencer, publication)
                        print("PUSH")
