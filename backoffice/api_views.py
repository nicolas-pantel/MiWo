from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from . import models
from . import serializers


class InfluencersAPIView(generics.ListAPIView):
    """Return the list of influencers"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.InfluencersSerializer

    def get_queryset(self):
        """Filter influencers only"""
        return models.MiwoUser.objects.filter(campaigns__isnull=False).distinct()


class InfluencersSearchAPIView(generics.ListAPIView):
    """Return list of influenceurs matching search_text"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.InfluencersSerializer

    def get_queryset(self):
        """Search for influencers containing search text"""
        return models.MiwoUser.objects.filter(
            campaigns__isnull=False, username__icontains=self.kwargs["search_text"]).distinct()


class InfluencerSubscriptionAPIView(APIView):
    """Subscribe user to influencer publications"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, influencer_pk, *args, **kwargs):
        """Add influencer to user subscriptions"""
        influencer = models.MiwoUser.objects.get(pk=influencer_pk)
        request.user.favorite_influencers.add(influencer)
        data = "User {} successfully subsribed to influencer {}".format(self.request.user.username, influencer_pk)
        return Response(data)


class InfluencersFavoritesAPIView(generics.ListAPIView):
    """Return user's favorite influencers"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.InfluencersSerializer

    def get_queryset(self):
        """Filter favorite influencers only"""
        return self.request.user.favorite_influencers.all()


class PublicationsAPIView(generics.ListAPIView):
    """Return the list of an influencer's publications"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PublicationsSerializer

    def get_queryset(self):
        """List of influencer's publications"""
        return models.Publication.objects.filter(campaign__user__pk=self.kwargs["influencer_pk"], published=True)


class TagsAPIView(generics.ListAPIView):
    """Return the list of tags linked to a publication"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TagsSerializer

    def get_queryset(self):
        """List of tags for a publication"""
        return models.TagVideo.objects.filter(publication__pk=self.kwargs["publication_pk"])


class TagAPIView(generics.RetrieveAPIView):
    """Return details of a tag linked to a publication"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TagSerializer
    queryset = models.TagVideo.objects.all()


class TagVideoFavoritesListView(TagsAPIView):
    """Return the list of favorited tags"""
    def get_queryset(self):
        return self.request.user.favorite_tags_video.all()


class TagVideoFavoriteAddView(APIView):
    """Add a favorite tag to a MiwoUser"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        """Add tag to user's favorites"""

        tag = get_object_or_404(models.TagVideo, pk=pk)
        request.user.favorite_tags_video.add(tag)
        data = "Tag {} successfully favorited by user {}".format(tag, self.request.user.username)
        return Response(data)


class TagVideoFavoriteRemoveView(APIView):
    """Remove a favorite tag from a MiwoUser"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        """Remove tag from user's favorites"""
        tag = get_object_or_404(models.TagVideo, pk=pk)
        request.user.favorite_tags_video.remove(tag)
        data = "Tag {} successfully removed by user {}".format(tag, self.request.user.username)
        return Response(data)
