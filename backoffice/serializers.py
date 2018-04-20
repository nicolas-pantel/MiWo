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

    class Meta:
        model = models.Publication
        fields = ('id_news', 'title_news', 'type', 'date', 'social_network')

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
        return ret


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = models.ProductImage
        fields = '__all__'


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
        ret['pics_produit'] = product['images'][0]
        return ret
