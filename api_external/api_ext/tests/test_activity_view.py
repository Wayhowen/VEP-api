import io
import json

from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_ext.tests.utils import login
from persistence.models import CustomUser, Patient

activity_url = reverse("activity")
to_remove = []


# TODO: need to restrict data to appriopriate people
class ActivityViewTestCase(APITestCase):
    def setUp(self):
        default_practitioner = CustomUser.objects.create(id=420,
                                                         email='pr@1.com',
                                                         phone_number=00000000000,
                                                         type='PR')
        default_patient_1 = CustomUser.objects.create(id=421,
                                                      email='pt@1.com',
                                                      phone_number=11000000000,
                                                      type='PT')
        default_patient_1_account = Patient.objects.create(id=423,
                                                           patient_account=default_patient_1)
        default_patient_2_account = Patient.objects.create(id=424,
                                                           patient_account=default_patient_1)

    def tearDown(self):
        while to_remove:
            id_to_remove = to_remove.pop()
            response = self.client.delete(reverse("activity", args=[id_to_remove]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activity_view_exists(self):
        """
        Check if activity view exists
        """
        tmp_file = self.generate_photo_file()

        data = {"file": tmp_file,
                "raw_recording": json.dumps({"test": "test"})}
        response = self.client.post(activity_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_uploading_files_works(self):
        """
        Check if activity view uploading files option works
        """
        tmp_file = self.generate_photo_file()

        data = {"file": tmp_file,
                "patient": 423,
                "feedback": "some feedback",
                "raw_recording": json.dumps({
                    "name": "test",
                    "start_time": 0,
                    "finish_time": 15,
                },
                )}
        login("default@default.com", "password", self.client)
        response = self.client.post(activity_url, data, format="multipart")
        to_remove.append(response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, response.data["id"])

        self.assertEqual("test", response.data["raw_recording"]["name"])
        self.assertEqual(0, response.data["raw_recording"]["start_time"])
        self.assertEqual(15, response.data["raw_recording"]["finish_time"])

        self.assertIn("file", response.data["raw_recording"])
        self.assertIn("test_file", response.data["raw_recording"]["file"])

        self.assertEqual(data["feedback"], response.data["feedback"])
        self.assertIn("processing_result", response.data)
        self.assertEqual(data["patient"], response.data["patient"])

    def test_uploading_doesnt_accept_missing_fields(self):
        """
        Check if activity view doesn't accept requests with missing fields
        """
        tmp_file = self.generate_photo_file()

        data = {"file": tmp_file,
                "raw_recording": json.dumps({
                    "name": "test",
                })}
        login("default@default.com", "password", self.client)
        response = self.client.post(activity_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("raw_recording", response.data)
        self.assertIn("start_time", response.data["raw_recording"])
        self.assertIn("finish_time", response.data["raw_recording"])
        self.assertIn("patient", response.data)

        self.assertNotIn("processing_result", response.data)
        self.assertNotIn("file", response.data["raw_recording"])
        self.assertNotIn("id", response.data)

    def test_activity_details_view_exists(self):
        """
        Check if activity details view exists
        """
        response = self.client.get(reverse("activity", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_activity_details_view_returns_correct_data(self):
        """
        Check if activity details view returns correct activity data
        """
        tmp_file = self.generate_photo_file()

        data = {"file": tmp_file,
                "patient": 423,
                "feedback": "some feedback",
                "raw_recording": json.dumps({
                    "name": "test",
                    "start_time": 0,
                    "finish_time": 15,
                },
                )}
        login("default@default.com", "password", self.client)
        response = self.client.post(activity_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        to_remove.append(response.data["id"])

        response = self.client.get(reverse("activity", args=[to_remove[0]]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data["id"])

        self.assertEqual("test", response.data["raw_recording"]["name"])
        self.assertEqual(1, response.data["raw_recording"]["id"])
        self.assertEqual(0, response.data["raw_recording"]["start_time"])
        self.assertEqual(15, response.data["raw_recording"]["finish_time"])

        self.assertIn("file", response.data["raw_recording"])
        self.assertIn("test_file", response.data["raw_recording"]["file"])

        self.assertEqual(data["feedback"], response.data["feedback"])
        self.assertIn("processing_result", response.data)
        self.assertEqual(data["patient"], response.data["patient"])

    def check_activity_update_view_exists(self):
        """
        Check if activity update view exists
        """
        response = self.client.put(reverse("activity", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_activity_update_view_allows_for_updates(self):
        """
        Check if activity update view updates all the activity details correctly
        """
        tmp_file = self.generate_photo_file()

        data = {"file": tmp_file,
                "patient": 423,
                "feedback": "some feedback",
                "raw_recording": json.dumps({
                    "name": "test",
                    "start_time": 0,
                    "finish_time": 15,
                },
                )}
        login("default@default.com", "password", self.client)
        response = self.client.post(activity_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        to_remove.append(response.data["id"])

        update_data = {"patient": 424,
                       "feedback": "other_feedback",
                       "file": "somefile",
                       "raw_recording": {
                           "name": "update test",
                           "start_time": 12,
                           "finish_time": 37,
                       }}

        response = self.client.put(reverse("activity", args=[to_remove[0]]), data=update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data["id"])

        self.assertEqual("update test", response.data["raw_recording"]["name"])
        self.assertEqual(1, response.data["raw_recording"]["id"])
        self.assertEqual(update_data["raw_recording"]["start_time"],
                         response.data["raw_recording"]["start_time"])
        self.assertEqual(update_data["raw_recording"]["finish_time"],
                         response.data["raw_recording"]["finish_time"])

        self.assertIn("file", response.data["raw_recording"])
        self.assertIn("test_file", response.data["raw_recording"]["file"])

        self.assertEqual(update_data["feedback"], response.data["feedback"])
        self.assertIn("processing_result", response.data)
        self.assertEqual(update_data["patient"], response.data["patient"])

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new("RGBA", size=(100, 100), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test_file.zip"
        file.seek(0)
        return file
