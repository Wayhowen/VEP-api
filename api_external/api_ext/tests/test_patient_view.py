from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_ext.tests.utils import login
from persistence.models import CustomUser, Patient


class PatientsViewTestCase(APITestCase):
    def setUp(self):
        # patients to lookup
        unrelated_patient_acc = CustomUser.objects.create(id=421,
                                                          email='unrelated@1.com',
                                                          phone_number=11000000000,
                                                          type='PT')
        default_patient_1_account = Patient.objects.create(id=423,
                                                           patient_account=unrelated_patient_acc)
        related_patient_acc = CustomUser.objects.create(id=424,
                                                        email='related@1.com',
                                                        phone_number=11100000000,
                                                        type='PT')
        default_patient_2_account = Patient.objects.create(id=425,
                                                           patient_account=related_patient_acc)

        # unrelated users
        self.client.post(reverse('users'), data={'email': 'pr@1.com', 'phone_number': '00000000000',
                                                 'user_type': 'PR', 'password': 'test1',
                                                 'assigned_patients': [425]})
        self.client.post(reverse('users'), data={'email': 'fm@1.com', 'phone_number': '00000000001',
                                                 'user_type': 'FM', 'password': 'test1',
                                                 'family_members': [424]})
        self.client.post(reverse('users'), data={'email': 'pt@1.com', 'phone_number': '00000000002',
                                                 'user_type': 'PT', 'password': 'test1',
                                                 'assigned_practitioner_id': 425})
        self.client.post(reverse('users'), data={'email': 'pr@1.com', 'phone_number': '00000000003',
                                                 'user_type': 'PR', 'password': 'test1'})

    def test_patients_view_exists(self):
        """
        Check if patients view exists
        """
        response = self.client.get(reverse('patients', args=[0]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patients_view_doesnt_return_data_for_unrelated_practitioner(self):
        login('pr@1.com', 'test1', self.client)
        response = self.client.get(reverse('patients', args=[423]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patients_view_doesnt_return_data_for_unrelated_patient(self):
        login('pt@1.com', 'test1', self.client)
        response = self.client.get(reverse('patients', args=[423]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patients_view_doesnt_return_data_for_unrelated_family_member(self):
        login('fm@1.com', 'test1', self.client)
        response = self.client.get(reverse('patients', args=[423]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patients_view_returns_data_for_related_practitioner(self):
        login('pr@1.com', 'test1', self.client)
        response = self.client.get(reverse('patients', args=[425]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 425)
        self.assertEqual(response.data["patient_account"], 424)
        self.assertEqual(response.data["assigned_practitioner"], 425)

    def test_patients_view_returns_data_for_same_patient(self):
        login('pt@1.com', 'test1', self.client)
        response = self.client.get(reverse('patients', args=[426]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 426)
        self.assertEqual(response.data["patient_account"], 427)
        self.assertEqual(response.data["assigned_practitioner"], 425)

    def test_patients_view_returns_data_for_related_family_member(self):
        login('fm@1.com', 'test1', self.client)
        response = self.client.get(reverse('patients', args=[425]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 425)
        self.assertEqual(response.data["patient_account"], 424)
        self.assertEqual(response.data["assigned_practitioner"], 425)
