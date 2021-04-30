from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_ext.tests.utils import login, check_sent_data
from persistence.models import Patient

fuzzy_setup_url = reverse("fuzzy_setup")


class FuzzySetupTestCase(APITestCase):
    def setUp(self):
        # TODO practitioner id is 3 but it might change, work it out
        response = self.client.post(reverse('users'),
                                    data={'email': 'pr@1.com', 'phone_number': '00000000000',
                                          'user_type': 'PR', 'password': 'test1'})

    def test_create_view_exists(self):
        """
        Check if a fuzzy logic create view exists
        """
        response = self.client.post(fuzzy_setup_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_view_accept_practitioner(self):
        """
        Check if a practitioner can access fuzzy logic create view
        """
        login("pr@1.com", "test1", self.client)
        response = self.client.post(fuzzy_setup_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_view_doesnt_accept_missing_fields(self):
        """
        Check if a fuzzy logic create view accepts missing fields
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": ""}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("patient", response.data)
        self.assertIn("rules", response.data)

    def test_create_view_doesnt_accept_wrong_type_of_rules(self):
        """
        Check if fuzzy logic create view accepts wrong type of rules
        """
        login("pr@1.com", "test1", self.client)

        data = {"rules": 1}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("rules", response.data)
        self.assertNotEqual(data["rules"], response.data["rules"])
        self.assertEqual(str(response.data["rules"][0]),
                         "Rules must be a list")

    def test_create_view_doesnt_accept_short_list_of_rules(self):
        """
        Check if fuzzy logic create view accepts too short list of rules
        """
        login("pr@1.com", "test1", self.client)

        data = {"rules": ["rule 1"]}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("rules", response.data)
        self.assertNotEqual(data["rules"], response.data["rules"])
        self.assertEqual(str(response.data["rules"][0]),
                         "There must be at least 2 rules")

    def test_create_view_doesnt_accept_wrong_type_of_object_in_rules_list(self):
        """
        Check if fuzzy logic create view accepts wrong type of objects in rules list
        """
        login("pr@1.com", "test1", self.client)

        data = {"rules": [1, 2, 3]}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("rules", response.data)
        self.assertNotEqual(data["rules"], response.data["rules"])
        self.assertEqual(str(response.data["rules"][0]),
                         "All list entries must be of type string")

    def test_create_view_accepts_correct_rules_list(self):
        """
        Check if fuzzy logic create view accepts correctly formatted rules list
        """
        login("pr@1.com", "test1", self.client)

        data = {"rules": ["rule 1", "rule 2"]}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("rules", response.data)

    def test_create_view_doesnt_accept_missing_patient(self):
        """
        Check if fuzzy logic create view accepts data with missing patient
        """
        login("pr@1.com", "test1", self.client)

        data = {"rules": ["rule 1", "rule 2"]}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("patient", response.data)
        self.assertEqual(str(response.data["patient"][0]),
                         "This field is required.")

    def test_create_view_doesnt_accept_null_patient(self):
        """
        Check if fuzzy logic create view accepts patient set as null
        """
        login("pr@1.com", "test1", self.client)

        data = {"patient": None}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("patient", response.data)
        self.assertEqual(str(response.data["patient"][0]),
                         "The patient cannot be null")

    def test_create_view_doesnt_accept_string_patient_id(self):
        """
        Check if fuzzy logic create view accepts wrong type of patient_id
        """
        login("pr@1.com", "test1", self.client)

        data = {"patient": "some"}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("patient", response.data)
        self.assertEqual(str(response.data["patient"][0]),
                         "Incorrect type. Expected pk value, received str.")

    def test_create_view_accepts_correct_patient(self):
        """
        Check if fuzzy logic create view accepts correctly formatted patient_id
        """
        login("pr@1.com", "test1", self.client)

        data = {"patient": 1}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("patient", response.data)

    def test_create_view_doesnt_allow_no_universes(self):
        """
        Check if fuzzy logic create view accepts missing universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "There must be at least one universe declared")

    def test_create_view_doesnt_allow_empty_universe(self):
        """
        Check if fuzzy logic create view accepts empty universes
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Universe test needs to have a range property")

    def test_create_view_doesnt_allow_wrong_range_type_in_range(self):
        """
        Check if fuzzy logic create view accepts wrong type in range in universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": 1}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Range property needs to be a list")

    def test_create_view_doesnt_allow_wrong_list_length_in_range(self):
        """
        Check if fuzzy logic create view accepts wrong list size in range in universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Range property  must contain exactly 3 elements")

    def test_create_view_doesnt_allow_not_numeric_values_in_range(self):
        """
        Check if fuzzy logic create view accepts wrong types of values in range in universes
         descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, "str"]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Range property can contain only numbers")

    def test_create_view_doesnt_allow_missing_membership_functions(self):
        """
        Check if fuzzy logic create view accepts missing membership functions in universes
         descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Universe test needs to have a membership_functions property")

    def test_create_view_doesnt_allow_membership_functions_to_be_of_wrong_type(self):
        """
        Check if fuzzy logic create view accepts wrong membership functions type in universes
         descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": 1}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "membership_functions property must be a list")

    def test_create_view_doesnt_allow_empty_membership_functions(self):
        """
        Check if fuzzy logic create view accepts empty membership functions in universes
         descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": []}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "membership_functions property must either have default value or function "
                         "description")

    def test_create_view_doesnt_allow_wrong_parameters_for_default_function(self):
        """
        Check if fuzzy logic create view accepts wrong parameters for default functions in universes
         descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "default": 4
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Membership functions default value must be either 3, 5 or 7")

    def test_create_view_allows_correctly_defined_default_function(self):
        """
        Check if fuzzy logic create view accepts correctly defined default function in universes
         descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "default": 3
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("universes_description", response.data)

    def test_create_view_doesnt_allow_missing_label_in_function(self):
        """
        Check if fuzzy logic create view accepts missing label for custom functions in universes
         descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Label property must be present for custom membership function")

    def test_create_view_custom_function_doesnt_allow_label_that_is_not_string(self):
        """
        Check if fuzzy logic create view accepts wrong type of label for custom functions in
        universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": 1
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Label must be a string instance")

    def test_create_view_custom_function_doesnt_allow_mising_type(self):
        """
        Check if fuzzy logic create view accepts missing type for custom functions in
        universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label"
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Type property must be present for custom membership function")

    def test_create_view_custom_function_doesnt_allow_wrong_function_type(self):
        """
        Check if fuzzy logic create view accepts wrong type for custom functions in
        universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "wrong_type"
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Type property must be either a triangle or trapezoid")

    def test_create_view_custom_function_doesnt_allow_missing_points(self):
        """
        Check if fuzzy logic create view accepts missing points for custom functions in
        universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle"
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Points property must be present for custom membership function")

    def test_create_view_custom_function_doesnt_allow_wrong_type_of_points(self):
        """
        Check if fuzzy logic create view accepts wrong type of points for custom functions in
        universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": 1
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Points property must be a list")

    def test_create_view_custom_function_doesnt_allow_wrong_points_number_for_function(self):
        """
        Check if fuzzy logic create view accepts wrong number of points for custom functions in
        universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3, 4]
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Points property must have length 3 for triangle")

    def test_create_view_custom_function_doesnt_allow_non_numeric_points(self):
        """
        Check if fuzzy logic create view accepts wrong type of points for custom functions in
        universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, "str", 3]
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("universes_description", response.data)
        self.assertEqual(str(response.data["universes_description"][0]),
                         "Each point in a list must be a numeric")

    def test_create_view_custom_function_allows_custom_function(self):
        """
        Check if fuzzy logic create view accepts correctly formatted custom function in
        universes descriptions
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}}}
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("universes_description", response.data)

    def test_create_view_accepts_correct_json(self):
        """
        Check if fuzzy logic create view accepts correctly formatted json
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}},
                "patient": 1,
                "rules": ["rule 1", "rule 2"]
                }
        response = self.client.post(fuzzy_setup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_sent_data(data, response, self.assertEqual)

    def test_get_view_exists(self):
        """
        Check if fuzzy logic get view exists
        """
        response = self.client.get(reverse("fuzzy_setup", args=[2]), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_view_works_for_practitioner(self):
        """
        Check if fuzzy logic get view works for practitioner
        """
        login("pr@1.com", "test1", self.client)
        response = self.client.get(reverse("fuzzy_setup", args=[2]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_view_return_default_for_missing_fuzzy_setup(self):
        """
        Check if fuzzy logic get view works returns default data for missing patient specific setup
        """
        login("pr@1.com", "test1", self.client)
        response = self.client.get(reverse("fuzzy_setup", args=[1]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(None, response.data["patient"])
        self.assertEqual(1, response.data["id"])

    def test_get_view_doesnt_return_data_for_unrelated_practitioner(self):
        """
        Check if fuzzy logic get view doesnt return data for unrelated practitioner
        """
        login("pr@1.com", "test1", self.client)

        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}},
                "patient": 1,
                "rules": ["rule 1", "rule 2"]
                }
        self.client.post(fuzzy_setup_url, data, format="json")

        response = self.client.get(reverse("fuzzy_setup", args=[1]), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_view_returns_data_for_related_practitioner(self):
        """
        Check if fuzzy logic get view returns data for related practitioner
        """
        login("pr@1.com", "test1", self.client)
        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}},
                "patient": 1,
                "rules": ["rule 1", "rule 2"]
                }
        self.client.post(fuzzy_setup_url, data, format="json")
        patient = Patient.objects.get(id=1)
        patient.assigned_practitioner_id = 3
        patient.save()

        response = self.client.get(reverse("fuzzy_setup", args=[1]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_sent_data(data, response, self.assertEqual)

    def test_edit_view_exists(self):
        """
        Check if fuzzy logic edit view exists
        """
        response = self.client.put(reverse("fuzzy_setup", args=[2]), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_view_works_for_practitioner(self):
        """
        Check if fuzzy logic edit view works for practitioner
        """
        login("pr@1.com", "test1", self.client)
        response = self.client.put(reverse("fuzzy_setup", args=[2]), format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_view_doesnt_allow_editing_for_unrelated_practitioner(self):
        """
        Check if fuzzy logic edit view doesnt allow editing for practitioner who is unrelated
        """
        login("pr@1.com", "test1", self.client)
        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}},
                "patient": 1,
                "rules": ["rule 1", "rule 2"]
                }
        self.client.post(fuzzy_setup_url, data, format="json")
        response = self.client.put(reverse("fuzzy_setup", args=[1]), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_view_allows_editing_for_related_practitioner(self):
        """
        Check if fuzzy logic edit view allows editing for related practitioner
        """
        login("pr@1.com", "test1", self.client)
        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}},
                "patient": 1,
                "rules": ["rule 1", "rule 2"]
                }
        self.client.post(fuzzy_setup_url, data, format="json")
        patient = Patient.objects.get(id=1)
        patient.assigned_practitioner_id = 3
        patient.save()

        login("pr@1.com", "test1", self.client)
        response = self.client.put(reverse("fuzzy_setup", args=[1]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_view_changes_objects_correctly(self):
        """
        Check if fuzzy logic edit allows for actual object modifications
        """
        login("pr@1.com", "test1", self.client)
        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}},
                "patient": 1,
                "rules": ["rule 1", "rule 2"]
                }
        self.client.post(fuzzy_setup_url, data, format="json")
        patient = Patient.objects.get(id=1)
        patient.assigned_practitioner_id = 3
        patient.save()

        update_data = {"universes_description": {"new_test": {"range": [2, 3, 4],
                                                              "membership_functions": [{
                                                                  "label": "new_label",
                                                                  "type": "trapezoid",
                                                                  "points": [4, 5, 6, 7]
                                                              }]}},
                       "patient": 1,
                       "rules": ["rule 2", "rule 3", "rule 4"]
                       }

        login("pr@1.com", "test1", self.client)
        response = self.client.put(reverse("fuzzy_setup", args=[1]), update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_sent_data(update_data, response, self.assertEqual)

    def test_edit_view_allows_partial_updates(self):
        """
        Check if fuzzy logic edit allows for partial object modifications
        """
        login("pr@1.com", "test1", self.client)
        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}},
                "patient": 1,
                "rules": ["rule 1", "rule 2"]
                }
        self.client.post(fuzzy_setup_url, data, format="json")
        patient = Patient.objects.get(id=1)
        patient.assigned_practitioner_id = 3
        patient.save()

        update_data = {
                       "rules": ["rule 2", "rule 3", "rule 4"]
                       }

        login("pr@1.com", "test1", self.client)
        response = self.client.put(reverse("fuzzy_setup", args=[1]), update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_sent_data(update_data, response, self.assertEqual)

    def test_edit_view_doesnt_allow_changing_id_or_patient_id(self):
        """
        Check if fuzzy logic edit doesnt allow changing read only properties
        """
        login("pr@1.com", "test1", self.client)
        data = {"universes_description": {"test": {"range": [1, 2, 3],
                                                   "membership_functions": [{
                                                       "label": "some_label",
                                                       "type": "triangle",
                                                       "points": [1, 2, 3]
                                                   }]}},
                "patient": 1,
                "rules": ["rule 1", "rule 2"]
                }
        create_response = self.client.post(fuzzy_setup_url, data, format="json")
        compare_to_data = create_response.data
        patient = Patient.objects.get(id=1)
        patient.assigned_practitioner_id = 3
        patient.save()

        update_data = {"id": 1020,
                       "patient": 16
                       }

        login("pr@1.com", "test1", self.client)
        response = self.client.put(reverse("fuzzy_setup", args=[1]), update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_sent_data(compare_to_data, response, self.assertEqual)
