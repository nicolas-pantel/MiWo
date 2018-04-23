from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from . import models


class MiwoModelTestCase(TestCase):
    def test_create_user(self):
        """On user creation, an empty profile must be created"""
        user = get_user_model().objects.create(username="test", email="test@test.com", password="test")
        self.assertIsNotNone(user.profile)


class PublicationModelTestCase(TestCase):
    def test_get_youtube_video_id_with_v(self):
        """Extract Youtube video id from url with 'v' parameter"""
        url = "https://www.youtube.com/watch?v=videoID"
        id = models.Publication().get_youtube_video_id(url)
        self.assertEqual(id, 'videoID')

    def test_get_youtube_video_id_with_multiple_parameters(self):
        """Extract Youtube video id from url with 'v' and other parameters"""
        url = "https://www.youtube.com/watch?v=videoID&feature=youtu.be"
        id = models.Publication().get_youtube_video_id(url)
        self.assertEqual(id, 'videoID')

    def test_get_youtube_video_id_without_v(self):
        """Extract Youtube video id from url without 'v' parameter"""
        url = "https://www.youtu.be/videoID"
        id = models.Publication().get_youtube_video_id(url)
        self.assertEqual(id, 'videoID')


class APITestCase(APITestCase):
    def test_create_user(self):
        """Must create a MiwoUser with email, password and a device"""
        # Test user
        user = models.MiwoUser.objects.create(email="test@test.com")
        user.set_password("test")
        user.save()
        # Login
        self.client.post(
            reverse("rest_login"), {"email": "test@test.com", "password": "test", "chanid": "aaabbb"})
        self.assertEqual(user.profile.devices.all()[0].chanid, "aaabbb")
