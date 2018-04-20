from rest_framework import serializers

from django.utils import timezone

from . import models


class ProfileSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()

    class Meta:
        model = models.Profile
        fields = '__all__'


class InfluencersSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = models.MiwoUser
        fields = ('pk', 'profile')

    def to_representation(self, instance):
        """Flatten profile."""
        ret = super().to_representation(instance)
        ret['username'] = ret['profile']['public_name']
        ret['candidat_picture'] = ret['profile']['picture']
        del ret['profile']
        return ret


class PublicationsSerializer(serializers.ModelSerializer):
    id_news = serializers.IntegerField(source="pk")
    title_news = serializers.CharField(source="name")
    type = serializers.CharField(source="pub_type")
    picture_news = serializers.ImageField(source="image")

    class Meta:
        model = models.Publication
        fields = ('id_news', 'title_news', 'type', 'date', 'picture_news', 'social_network')

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
        return ret
