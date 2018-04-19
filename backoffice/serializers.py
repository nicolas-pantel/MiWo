from rest_framework import serializers

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
