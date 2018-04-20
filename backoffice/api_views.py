from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


class InfluencersAPIView(generics.ListAPIView):
    """Return the list of influencers"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.InfluencersSerializer

    def get_queryset(self):
        """Filter influencers only"""
        return models.MiwoUser.objects.filter(campaigns__isnull=False).distinct()
'''
    def get(self, request, *args, **kwargs):
        """Return the list of influencers"""
        data = [
            {"pk": 1, "username": "influencer 1", "candidat_picture": "https://loremflickr.com/150/150/face?lock=1"},
            {"pk": 2, "username": "influencer 2", "candidat_picture": "https://loremflickr.com/150/150/face?lock=2"},
            {"pk": 3, "username": "influencer 3", "candidat_picture": "https://loremflickr.com/150/150/face?lock=3"},
        ]
        return Response(data)
'''


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
'''
    def get(self, request, *args, **kwargs):
        """Return user's favorite influencers"""
        data = [
            {"pk": 1, "username": "influencer 1", "candidat_picture": "https://loremflickr.com/150/150/face?lock=1"},
            {"pk": 2, "username": "influencer 2", "candidat_picture": "https://loremflickr.com/150/150/face?lock=5"},
            {"pk": 3, "username": "influencer 3", "candidat_picture": "https://loremflickr.com/150/150/face?lock=6"},
        ]
        return Response(data)
'''


class InfluencersSearchAPIView(generics.ListAPIView):
    """Return list of influenceurs matching search_text"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.InfluencersSerializer

    def get_queryset(self):
        """Search for favorite influencers containing search text"""
        return self.request.user.favorite_influencers.filter(username__icontains=self.kwargs["search_text"])
'''
    def get(self, request, search_text, *args, **kwargs):
        """Return list of influenceurs matching search_text"""
        data = [
            {
                "pk": 5, "username": "{} the influ".format(search_text),
                "candidat_picture": "https://loremflickr.com/150/150/face?lock=1"},
            {
                "pk": 8, "username": "super{}".format(search_text),
                "candidat_picture": "https://loremflickr.com/150/150/face?lock=6"},
            {
                "pk": 9, "username": "top_{}_x".format(search_text),
                "candidat_picture": "https://loremflickr.com/150/150/face?lock=7"},
        ]
        return Response(data)
'''


class PublicationsAPIView(generics.ListAPIView):
    """Return the list of an influencer's publications"""
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PublicationsSerializer

    def get_queryset(self):
        """List of influencer's publications"""
        return models.Publication.objects.filter(campaign__user__pk=self.kwargs["influencer_pk"])

'''
    def get(self, request, influencer_pk, *args, **kwargs):
        """Return the list of an influencer's publications"""
        data = [
            {
                "id_news": 10, "title_news": "First pub of influ {}".format(influencer_pk), "type": "video",
                "date_news": "April 21, 2018", "picture_news": "https://loremflickr.com/150/150/youtube?lock=1",
                "nb_products": "2 products", "timeline_value": 25, "social_network": "youtube",
            },
            {
                "id_news": 11, "title_news": "Second pub of influ {}".format(influencer_pk), "type": "video",
                "date_news": "April 23, 2018", "picture_news": "https://loremflickr.com/150/150/youtube?lock=2",
                "nb_products": "5 products", "timeline_value": 12, "social_network": "youtube",
            },
            {
                "id_news": 13, "title_news": "Third pub of influ {}".format(influencer_pk), "type": "video",
                "date_news": "April 24, 2018", "picture_news": "https://loremflickr.com/150/150/youtube?lock=3",
                "nb_products": "1 products", "timeline_value": 2, "social_network": "youtube",
            },
        ]
        return Response(data)
'''


class TagsAPIView(APIView):
    """Return the list of tags linked to a publication"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, publication_pk, *args, **kwargs):
        """Return the list of tags linked to a publication"""
        data = [
            {
                # "pk": 20, "title": "First tag of publi {}".format(publication_pk),
                "id_product": 20, "nom_product": "Shoe",
                "desc_product": "White striped shoes. Sportswear.",
                "prix_produit": 120,
                "pics_produit": "https://loremflickr.com/150/150/shoe?lock=3"},
            {
                # "pk": 21, "title": "Second tag of publi {}".format(publication_pk),
                "id_product": 205, "nom_product": "Hat",
                "desc_product": "Red hat.",
                "prix_produit": 35,
                "pics_produit": "https://loremflickr.com/150/150/cat?lock=6"},
            {
                # "pk": 22, "title": "Third tag of publi {}".format(publication_pk),
                "id_product": 207, "nom_product": "Jacket",
                "desc_product": "Blue jacket. Sportswear.",
                "prix_produit": 120,
                "pics_produit": "https://loremflickr.com/150/150/cat?lock=1"},
        ]
        return Response(data)


class TagAPIView(APIView):
    """Return details of a tag linked to a publication"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, publication_pk, tag_pk, *args, **kwargs):
        """Return details of a tag linked to a publication"""
        data = {
            "pk": 20, "title": "First tag of publi {}".format(publication_pk),
            "id_product": 20,
            "nom_product": "Shoe", "product_price": 70,
            "desc_product": "White striped shoes. Sportswear.",
            "prix_produit": 120,
            "pics_produit": [
                'https://loremflickr.com/500/500/shoe?lock=3',
                'https://loremflickr.com/500/500/shoes?lock=4',
                'https://loremflickr.com/500/500/shoes?lock=5',
            ],
            "purchase_link": "http://vendor.com/products/shoe/",
        }
        return Response(data)
