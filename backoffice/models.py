from urllib.parse import urlparse, parse_qs

from cloudinary.models import CloudinaryField

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """User attached profile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    picture = CloudinaryField('image', blank=True, null=True)
    public_name = models.CharField(_("Public name"), max_length=150)

    def __str__(self):
        return "{}".format(self.public_name)

    def get_absolute_url(self):
        return reverse('profile_update', args=[str(self.id)])


class Campaign(models.Model):
    """Ads campaign"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(_("Name"), max_length=150)

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('campaigns')


class Product(models.Model):
    """Advertised products"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(_("Name"), max_length=150)
    description = models.TextField(_("Description"))
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('product_update', kwargs={"pk": self.pk})


class ProductImage(models.Model):
    """Image linked to a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image', blank=True, null=True)


class Publication(models.Model):
    """Influencer publication"""
    VIDEO = 'video'
    TYPES = (
        (VIDEO, _("Video")),
    )

    YOUTUBE = 'youtube'
    SOCIAL_NETWORKS = (
        (YOUTUBE, _("Youtube")),
    )
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="publications")
    name = models.CharField(_("Title"), max_length=150)
    url = models.URLField("Url")
    pub_type = models.CharField(_("Type"), max_length=50, choices=TYPES, default=VIDEO)
    social_network = models.CharField(_("Social network"), max_length=150, choices=SOCIAL_NETWORKS, default=YOUTUBE)
    date = models.DateTimeField(_("Date"), default=timezone.now)
    expiration_date = models.DateTimeField(_("Expiration date"), default=timezone.now() + timezone.timedelta(days=7))
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('publications', kwargs={"campaign_pk": self.campaign.pk})

    def get_youtube_video_id(self, url):
        # Case http(s)://www.youtube.com/watch?v=videoID&feature=youtu.be
        parsed_url = urlparse(url)
        parameters = parse_qs(parsed_url.query)
        if parameters.get('v'):
            return parameters.get('v')[0]
        # Case http(s)://www.youtu.be/videoID
        return url.split('/')[-1]

    def get_youtube_embed_url(self):
        return "https://www.youtube.com/embed/{}".format(self.get_youtube_video_id(self.url))

    def get_youtube_thumbnail(self):
        return "https://img.youtube.com/vi/{}/0.jpg".format(self.get_youtube_video_id(self.url))


class TagVideo(models.Model):
    """Tag for video publication"""
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="tags_video")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tags")
    timestamp = models.TimeField('Timestamp')

    def __str__(self):
        return "{} {}".format(self.publication.name, self.timestamp)

    def get_absolute_url(self):
        return reverse('tagvideo_create', kwargs={"publication_pk": self.publication.pk})


class MiwoUser(AbstractUser):
    favorite_influencers = models.ManyToManyField("self", symmetrical=False)
    favorite_tags_video = models.ManyToManyField(TagVideo, symmetrical=False)

    def save(self, *args, **kwargs):
        """On user creation, add a profile."""
        if not self.pk:
            super().save(*args, **kwargs)
            profile = Profile.objects.create(user=self, public_name=self.username)
            profile.save()
        else:
            super().save(*args, **kwargs)
