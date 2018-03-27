from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class InfluencersAPIView(APIView):
    """Return the list of influencers"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Return the list of influencers"""
        data = [
            {"pk": 1, "username": "influencer 1", "image_url": "http://example.com/image1"},
            {"pk": 2, "username": "influencer 2", "image_url": "http://example.com/image2"},
            {"pk": 3, "username": "influencer 3", "image_url": "http://example.com/image3"},
        ]
        return Response(data)


class InfluencersFavoritesAPIView(APIView):
    """Return user's favorite influencers"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Return user's favorite influencers"""
        data = [
            {"pk": 1, "username": "influencer 1", "image_url": "http://example.com/image1"},
            {"pk": 2, "username": "influencer 2", "image_url": "http://example.com/image2"},
            {"pk": 3, "username": "influencer 3", "image_url": "http://example.com/image3"},
        ]
        return Response(data)


class InfluencersSearchAPIView(APIView):
    """Return list of influenceurs matching search_text"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, search_text, *args, **kwargs):
        """Return list of influenceurs matching search_text"""
        data = [
            {"pk": 5, "username": "{} the influ".format(search_text), "image_url": "http://example.com/image5"},
            {"pk": 8, "username": "super{}".format(search_text), "image_url": "http://example.com/image8"},
            {"pk": 9, "username": "top_{}_x".format(search_text), "image_url": "http://example.com/image9"},
        ]
        return Response(data)


class InfluencerSubscriptionAPIView(APIView):
    """Subscribe user to influencer publications"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, influencer_pk, *args, **kwargs):
        """Add influencer to user subscriptions"""
        data = "User {} successfully subsribed to influencer {}".format(self.request.user.username, influencer_pk)
        return Response(data)


class PublicationsAPIView(APIView):
    """Return the list of an influencer's publications"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, influencer_pk, *args, **kwargs):
        """Return the list of an influencer's publications"""
        data =[
            {
                "pk": 10, "title": "First pub of influ {}".format(influencer_pk), "type": "video",
                "image_url": "http://example.com/image10"
            },
            {
                "pk": 11, "title": "Second pub of influ {}".format(influencer_pk), "type": "video",
                "image_url": "http://example.com/image11"
            },
            {
                "pk": 13, "title": "Third pub of influ {}".format(influencer_pk), "type": "video",
                "image_url": "http://example.com/image13"
            },
        ]
        return Response(data)


class TagsAPIView(APIView):
    """Return the list of tags linked to a publication"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, influencer_pk, publication_pk, *args, **kwargs):
        """Return the list of tags linked to a publication"""
        data =[
            {"pk": 20, "title": "First tag of publi {}".format(publication_pk), "image_url": "http://example.com/image20"},
            {"pk": 21, "title": "Second tag of publi {}".format(publication_pk), "image_url": "http://example.com/image21"},
            {"pk": 22, "title": "Third tag of publi {}".format(publication_pk), "image_url": "http://example.com/image22"},
        ]
        return Response(data)


class TagAPIView(APIView):
    """Return details of a tag linked to a publication"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, influencer_pk, publication_pk, tag_pk, *args, **kwargs):
        """Return details of a tag linked to a publication"""
        data = {
            "pk": 20, "title": "First tag of publi {}".format(publication_pk),
            "product_name": "Shoe", "product_price": 70,
            "image_url": "http://example.com/image20",
            "purchase_link": "http://vendor.com/products/shoe/",
        }
        return Response(data)
