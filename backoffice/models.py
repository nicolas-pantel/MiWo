from cloudinary.models import CloudinaryField

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """User attached profile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    picture = CloudinaryField('image')
    public_name = models.CharField(_("Public name"), max_length=150)
