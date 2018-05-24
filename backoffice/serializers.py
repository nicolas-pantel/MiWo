from rest_auth import serializers as rest_auth_serializers
from rest_auth.registration import serializers as rest_auth_registration_serializers
from rest_framework import serializers

from django.utils import timezone

from . import models


def image_url_resize(url, width, heigh):
    file = url.split("/")[-2]
    return url.split(file)[0] + "c_fill,h_{},w_{}/".format(width, heigh) + file


class ProfileSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()

    class Meta:
        model = models.Profile
        fields = '__all__'


class RegisterSerializer(rest_auth_registration_serializers.RegisterSerializer):
    chanid = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.chanid = attrs["chanid"]
        return attrs

    def save(self, request):
        user = super().save(request)
        # If the user is logged in, register its device
        device, create = models.Device.objects.get_or_create(profile=user.profile)
        device.chanid = self.chanid
        device.save()
        return user


class LoginSerializer(rest_auth_serializers.LoginSerializer):
    chanid = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # If the user is logged in, register its device
        user = attrs["user"]
        chanid = attrs.get("chanid")
        device, create = models.Device.objects.get_or_create(profile=user.profile)
        device.chanid = chanid
        device.save()
        return attrs


class InfluencersSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = models.MiwoUser
        fields = ('pk', 'username', 'profile')

    def to_representation(self, instance):
        """Flatten profile."""
        ret = super().to_representation(instance)
        ret['candidat_picture'] = ret['profile']['picture']
        del ret['profile']
        return ret


class PublicationsSerializer(serializers.ModelSerializer):
    id_news = serializers.IntegerField(source="pk")
    title_news = serializers.CharField(source="name")
    type = serializers.CharField(source="pub_type")

    class Meta:
        model = models.Publication
        fields = ('id_news', 'title_news', 'type', 'date', 'social_network', 'url')

    def to_representation(self, instance):
        """Convert some fields to client format."""
        ret = super().to_representation(instance)
        ret['date_news'] = instance.date.strftime("%B %d, %Y")
        del ret['date']
        nb_product = instance.tags_video.count()
        if nb_product > 1:
            ret['nb_product'] = "{} products".format(nb_product)
        else:
            ret['nb_product'] = "{} product".format(nb_product)
        ret['timeline_value'] = (
            int((instance.expiration_date - timezone.now()) / (instance.expiration_date - instance.date) * 100)
        )
        ret['picture_news'] = instance.get_youtube_thumbnail()
        ret['youtube_video_id'] = instance.get_youtube_video_id(instance.url)
        ret['influencer'] = instance.campaign.user.username
        if instance.campaign.user.profile.picture is not None:
            ret['influencer_image_url'] = image_url_resize(instance.campaign.user.profile.picture.url, 50, 50)
        else:
            ret['influencer_image_url'] = ""
        return ret


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = models.ProductImage
        fields = ('image',)

    def to_representation(self, instance):
        """Return only image"""
        ret = super().to_representation(instance)
        return ret["image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = models.Product
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = models.TagVideo
        fields = ('pk', 'product')

    def to_representation(self, instance):
        """Return product's stuff"""
        ret = super().to_representation(instance)
        # For now client doesn't consider tags. Mimic product only infos.
        ret['id_product'] = ret['pk']
        del ret['pk']
        product = ret['product']
        del ret['product']
        ret['nom_product'] = product['name']
        ret['desc_product'] = product['description']
        ret['prix_produit'] = product['price']
        if product['images']:
            image_url = product['images'][0]
            if image_url:
                ret['pics_produit'] = image_url_resize(image_url, 150, 150)
            else:
                ret['pics_produit'] = image_url
        else:
            ret['pics_produit'] = ""
        ret['youtube_video_id'] = instance.publication.get_youtube_video_id()
        ret['timestamp'] = instance.timestamp
        ret['news_name'] = instance.publication.name
        ret['influencer'] = instance.publication.campaign.user.username
        if instance.publication.campaign.user.profile.picture is not None:
            ret['influencer_image_url'] = image_url_resize(
                instance.publication.campaign.user.profile.picture.url, 50, 50)
        else:
            ret['influencer_image_url'] = ""
        return ret


class TagSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = models.TagVideo
        fields = ('pk', 'product', 'timestamp')

    def to_representation(self, instance):
        """Return product's stuff"""
        ret = super().to_representation(instance)
        # For now client doesn't consider tags. Mimic product only infos.
        ret['id_product'] = ret['pk']
        del ret['pk']
        product = ret['product']
        del ret['product']
        ret['nom_product'] = product['name']
        ret['desc_product'] = product['description']
        ret['prix_produit'] = product['price']
        ret['pics_produit'] = product["images"]
        ret['referal_link'] = product["referal_link"]
        ret['influencer'] = instance.publication.campaign.user.username
        if instance.publication.campaign.user.profile.picture is not None:
            ret['influencer_image_url'] = image_url_resize(
                instance.publication.campaign.user.profile.picture.url, 50, 50)
        else:
            ret['influencer_image_url'] = ""
        return ret
