from cloudinary.models import CloudinaryField

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class MiwoUser(AbstractUser):

    def save(self, *args, **kwargs):
        """On user creation, add a profile."""
        if not self.pk:
            super().save(*args, **kwargs)
            profile = Profile.objects.create(user=self, public_name=self.username)
            profile.save()
        else:
            super().save(*args, **kwargs)


class Profile(models.Model):
    """User attached profile"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    picture = CloudinaryField('image', blank=True, null=True)
    public_name = models.CharField(_("Public name"), max_length=150)

    def get_absolute_url(self):
        return reverse('profile_update', args=[str(self.id)])


class Campaign(models.Model):
    """Ads campaign"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(_("Name"), max_length=150)

    class Meta:
        unique_together = ("user", "name")

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

    def get_absolute_url(self):
        return reverse('product_update', kwargs={"pk": self.pk})


class ProductImage(models.Model):
    """Image linked to a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image', blank=True, null=True)


class Publication(models.Model):
    """Influencer publication"""
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="publications")
    url = models.URLField("Url")
