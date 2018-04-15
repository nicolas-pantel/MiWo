from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelsTestCase(TestCase):
    def test_create_user(self):
        """On user creation, an empty profile must be created"""
        user = get_user_model().objects.create(username="test", email="test@test.com", password="test")
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.public_name, "test")

    def test_no_create_user_on_update(self):
        """On user update, do not modify profile"""
        user = get_user_model().objects.create(username="test", email="test@test.com", password="test")
        user.profile.public_name = "new profile name"
        user.profile.save()
        user.username = "new username"
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.profile.public_name, "new profile name")
