import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_ext.tests.utils import check_sent_data, login

job_url = reverse('job')
job_details_url = reverse('job_details', args=[1])


# TODO: think of other ways to test swagger output
class SwaggerTestCase(APITestCase):
    def setUp(self):
        self.client.post(reverse('users'), data={'email': 'pr@1.com', 'phone_number': '00000000000',
                                                 'user_type': 'PR', 'password': 'test1'})
        self.client.post(reverse('users'), data={'email': 'fm@1.com', 'phone_number': '10000000000',
                                                 'user_type': 'FM', 'password': 'test2'})
        self.client.get(reverse('logout'))

    def test_job_view_exists(self):
        """
        Check if job view exists
        """
        data = {}
        response = self.client.post(job_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_unavailable_without_correct_permissions(self):
        """
        Check if job is unavailable unless user is logged in with appropriate permissions
        """
        login('fm@1.com', 'test2', self.client)
        data = {}
        response = self.client.post(job_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_available_after_logging_in(self):
        """
        Check if creating jobs is available to logged in users
        """
        login('pr@1.com', 'test1', self.client)
        data = {'type': 2, 'patient_id': 1}
        response = self.client.post(job_url, data)
        check_sent_data(data, response, self.assertEqual)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("uid", response.data)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["activity_result"], None)

    def test_job_details_view_exists(self):
        """
        Check if job details view exists
        """
        response = self.client.get(job_details_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_details_unavailable_without_permissions(self):
        """
        Check if job details are unavailable without correct permissions
        """
        login('fm@1.com', 'test2', self.client)
        response = self.client.get(job_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_job_details_available_after_logging_in(self):
        """
        Check if job details are available to users with permissions
        """
        login('pr@1.com', 'test1', self.client)

        data = {'type': 2, 'patient_id': 1}
        created_job_response = self.client.post(job_url, data)

        response = self.client.get(reverse('job_details', args=[created_job_response.data['uid']]),
                                    data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data.pop('type')
        check_sent_data(data, response, self.assertEqual)
        self.assertIn("status", response.data)
        self.assertEqual(response.data["start_datetime"], None)
        self.assertEqual(response.data["finish_datetime"], None)
        self.assertEqual(response.data["error_message"], None)
        self.assertIn("activity_result_id", response.data)

    def test_updating_job_details_possible(self):
        """
        Check if job details are available to users with permissions
        """
        login('pr@1.com', 'test1', self.client)

        data = {'type': 2, 'patient_id': 1}
        created_job_response = self.client.post(job_url, data)

        update_data = {"start_datetime": datetime.datetime.now(),
                       "finish_datetime": datetime.datetime.now() + datetime.timedelta(hours=9),
                       "error_message": "Some error"}
        response = self.client.put(reverse('job_details', args=[created_job_response.data['uid']]),
                                    update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        check_sent_data(update_data, response, self.assertEqual)
        self.assertIn("status", response.data)
        self.assertIn("activity_result_id", response.data)
