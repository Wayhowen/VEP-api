from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


swagger_url = reverse('schema-swagger-ui')


# TODO: think of other ways to test swagger output
class SwaggerTestCase(APITestCase):
    def test_view_exists(self):
        """
        Check if swagger view exists
        """
        response = self.client.get(swagger_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
