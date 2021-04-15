from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_ext.tests.utils import login

raw_recording_url = reverse('raw_recording')


# TODO: need to check if this view returns appriopriate data
class RawRecordingTestCase(APITestCase):
    def setUp(self):
        self.client.post(reverse('users'), data={'email': 'pr@1.com', 'phone_number': '00000000000',
                                                 'user_type': 'PR', 'password': 'test1'})

    def test_view_exists(self):
        """
        Check if raw recording view exists
        """
        response = self.client.post(raw_recording_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_works_for_logged_in_users(self):
        """
        Check if raw recording view exists
        """
        login('pr@1.com', 'test1', self.client)
        response = self.client.post(raw_recording_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
