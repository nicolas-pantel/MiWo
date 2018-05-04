from django.core.management.base import BaseCommand

from backoffice import models
from backoffice.external_api_clients import youtube


class Command(BaseCommand):
    help = 'Query Youtube API for private videos status'

    def handle(self, *args, **options):
        print("youtube management command")
        # For each influencer
        influencers = models.MiwoUser.objects.filter(campaigns__isnull=False).distinct()
        for influencer in influencers:
            print(influencer.username)
            # Query YT for influencer's private videos
            if influencer.socialaccount_set.filter(provider="google"):
                publications = models.Publication.objects.filter(campaign__user=influencer, published=False)
                videos_ids = [publication.get_youtube_video_id() for publication in publications]
                status = youtube.videos_status(influencer, videos_ids)
                print(status)
