from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.token_url = reverse("token_obtain_pair")
        self.profile_url = reverse("profile")
        self.user_data = {
            "username": "testcandidate",
            "email": "candidate@example.com",
            "password": "Password123!",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testcandidate").exists())

    def test_jwt_login_and_profile_access(self):
        # Register user first
        self.client.post(self.register_url, self.user_data, format="json")

        # Obtain JWT
        login_res = self.client.post(
            self.token_url,
            {"username": "testcandidate", "password": "Password123!"},
            format="json",
        )
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_res.data)

        # Access profile with token
        access_token = login_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        profile_res = self.client.get(self.profile_url)
        self.assertEqual(profile_res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_res.data["username"], "testcandidate")
