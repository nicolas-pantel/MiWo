from urllib.parse import urlparse, parse_qs

from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy


class Profile(models.Model):
    """User attached profile"""
    INFLUENCER = "I"
    AGENCY = "A"
    PLATFORM = "P"
    KIND = (
        (INFLUENCER, _("Influencer")),
        (AGENCY, _("Agency")),
        (PLATFORM, _("Platform")),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    picture = CloudinaryField('image', blank=True, null=True)
    kind = models.CharField(_("Kind"), max_length=1, choices=KIND, blank=True, null=True)
    company_name = models.CharField(_("Company name"), max_length=150, blank=True, null=True)
    country = CountryField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.user.username)

    def get_absolute_url(self):
        return reverse('profile_update', args=[str(self.id)])


class Device(models.Model):
    """A user device"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="device")
    chanid = models.CharField(_("Chan id"), max_length=100)


class Campaign(models.Model):
    """Ads campaign"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(_("Name"), max_length=150)

    class Meta:
        unique_together = ("user", "name")
        ordering = ['-pk']

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('campaigns')


class Product(models.Model):
    """Advertised products"""
    ENTERTAINMENT = "entertainment"
    SPORT = "sport"
    CULTURE = "culture"
    CATEGORIES = (
        (ENTERTAINMENT, _("Entertainment")),
        (SPORT, _("Sport")),
        (CULTURE, _("Culture")),
    )
    FASHION = "fashion"
    MAKEUP = "makeup"
    SUB_CATEGORIES = (
        (FASHION, _("Fashion")),
        (MAKEUP, _("Makeup")),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(pgettext_lazy("Name", "Product"), max_length=150)
    legend = models.CharField(_("Legend"), max_length=100, null=True, blank=True)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Price"), max_digits=7, decimal_places=2)
    category = models.CharField(_("Category"), max_length=100, choices=CATEGORIES, default=ENTERTAINMENT)
    sub_category = models.CharField(_("Subcategory"), max_length=100, choices=SUB_CATEGORIES, default=FASHION)
    date_from = models.DateTimeField(_("From"), default=timezone.now)
    date_to = models.DateTimeField(_("To"), default=timezone.now() + timezone.timedelta(days=7))
    referal_link = models.URLField(_("Referal link"), max_length=150, null=True, blank=True)

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
    name = models.CharField(_("Title"), max_length=150, null=True, blank=True)
    url = models.URLField("Url")
    video_id = models.CharField(_("Video ID"), max_length=15, null=True, blank=True)
    pub_type = models.CharField(_("Type"), max_length=50, choices=TYPES, default=VIDEO)
    social_network = models.CharField(_("Social network"), max_length=150, choices=SOCIAL_NETWORKS, default=YOUTUBE)
    date = models.DateTimeField(_("Date"), default=timezone.now)
    expiration_date = models.DateTimeField(_("Expiration date"), default=timezone.now() + timezone.timedelta(days=7))
    image = CloudinaryField('image', blank=True, null=True)
    published = models.BooleanField(_("Published"), default=False)

    def __str__(self):
        return "{}".format(self.url)

    def save(self, *args, **kwargs):
        self.video_id = self.get_youtube_video_id()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('campaigns')

    def get_youtube_video_id(self, url=None):
        # Case http(s)://www.youtube.com/watch?v=videoID&feature=youtu.be
        if url is None:
            url = self.url
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
    favorite_influencers = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    favorite_tags_video = models.ManyToManyField(TagVideo, symmetrical=False)

    def save(self, *args, **kwargs):
        """On user creation, add a profile."""
        if not self.pk:
            super().save(*args, **kwargs)
            profile = Profile.objects.create(user=self)
            profile.save()
        else:
            super().save(*args, **kwargs)
