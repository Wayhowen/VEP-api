from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

login_url = reverse('login')
logout_url = reverse('logout')


class AuthenticationAuthorizationTestCase(APITestCase):
    def test_login(self):
        """
        Check if user can log in
        """
        data = {"email": "default@default.com", "password": "password"}
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_doesnt_work_for_wrong_credentials(self):
        """
        Check if user can't log in with wrong credentials
        """
        data = {"email": "wrong@wrong.com", "password": "notapwd"}
        response = self.client.post(login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_works(self):
        """
        Check if user can log out
        """
        data = {"email": "default@default.com", "password": "password"}
        self.client.post(login_url, data)
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_doesnt_work_for_user_that_is_not_logged_in(self):
        """
        Check if user can't log out if not logged in
        """
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
