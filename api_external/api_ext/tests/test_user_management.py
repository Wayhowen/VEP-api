from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from persistence.models import CustomUser, Patient
from api_ext.tests.utils import check_sent_data

creation_url = reverse('users')
# update_url = reverse('users_details')


# TODO: add user editing, updating, deleting and check if some fields return errors
class UserManagementTestCase(APITestCase):
    def setUp(self):
        default_practitioner = CustomUser.objects.create(id=420,
                                                         email='pr@1.com',
                                                         phone_number=00000000000,
                                                         type='PR')
        default_family_member = CustomUser.objects.create(id=421,
                                                          email='fm@1.com',
                                                          phone_number=10000000000,
                                                          type='FM')
        default_patient_1 = CustomUser.objects.create(id=422,
                                                      email='pt@1.com',
                                                      phone_number=11000000000,
                                                      type='PT')
        default_patient_1_account = Patient.objects.create(id=423,
                                                           patient_account=default_patient_1)
        default_practitioner.save()

    # TODO: Might add error validation
    def test_insufficient_data_doesnt_create_user(self):
        """
        Check if sending insufficient data actually creates user
        """
        data = {'insufficient': 'data'}
        response = self.client.post(creation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_practitioner_works(self):
        """
        Check if practitioner creation works
        """
        data = {'email': 'test@email.com', 'phone_number': '99999999999', 'user_type': 'PR',
                'assigned_patients': [423]}
        response = self.client.post(creation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_sent_data(data, response, self.assertEqual)
        self.assertIn("patient_id", response.data)
        self.assertEqual(response.data["patient_id"], None)

    def test_creating_patient_works(self):
        """
        Check if patient creation works
        """
        data = {'email': 'test@email.com', 'phone_number': '99999999999', 'user_type': 'PT',
                'assigned_practitioner_id': 420, 'family_members': [421]}
        response = self.client.post(creation_url, data, format='json')

        cu = CustomUser.objects.get(id=response.data['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_sent_data(data, response, self.assertEqual)
        self.assertIn("patient_id", response.data)
        self.assertNotEqual(response.data["patient_id"], None)

    def test_creating_family_members_works(self):
        """
        Check if family member creation works
        """
        data = {'email': 'test@email.com', 'phone_number': '99999999999', 'user_type': 'FM',
                'family_members': [422]}
        response = self.client.post(creation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_sent_data(data, response, self.assertEqual)
        self.assertIn("patient_id", response.data)
        self.assertEqual(response.data["patient_id"], None)

    def test_creating_system_administrator_works(self):
        """
        Check if system administrator creation works
        """
        data = {'email': 'test@email.com', 'phone_number': '99999999999', 'user_type': 'SA'}
        response = self.client.post(creation_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_sent_data(data, response, self.assertEqual)
        self.assertIn("patient_id", response.data)
        self.assertEqual(response.data["patient_id"], None)
