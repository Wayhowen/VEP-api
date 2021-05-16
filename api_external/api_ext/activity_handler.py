from django.shortcuts import get_list_or_404
from rest_framework.request import Request

from persistence.models import ActivityResult, RawRecording


class Handler:
    def __init__(self):
        pass

    def process(self, request: Request) -> dict:
        dict_query = dict(request.data)

        query = ActivityResult.objects.all()

        if patient_email := dict_query.get("patient_email", None):
            query = ActivityResult.objects.filter(
                patient__patient_account__email=patient_email)
        elif patient_id := dict_query.get("patient_id", None):
            query = ActivityResult.objects.filter(
                patient__id=patient_id)
        elif activity_id := dict_query.get("activity_id", None):
            query = ActivityResult.objects.filter(
                id=activity_id)

        if "activity_name" in dict_query:
            query = query.filter(name=dict_query["activity_name"])
        if "timestamp_from" in dict_query:
            query = query.filter(start_time__gte=dict_query["timestamp_from"])
        if "timestamp_to" in dict_query:
            query = query.filter(start_time__lte=dict_query["timestamp_to"])
        response_data = {"activity_results": self._create_response_dicts_list(get_list_or_404(query))}
        return response_data

    def _create_response_dicts_list(self, objects):
        response_dicts_list = []
        for activity in objects:
            activity_dict = dict()
            activity_dict[activity.id] = {
                "feedback": activity.feedback,
                "raw_recording_id": activity.raw_recording_id,
                "processing_result": activity.processing_result,
                "preprocessing_result": activity.preprocessing_result
            }
            response_dicts_list.append(activity_dict)
        return response_dicts_list

    def _choose_handler(self, user_type):
        if user_type == "PT":
            self._handle_practitioner()
        elif user_type == "FM":
            self._handle_family_member()
        elif user_type == "PT":
            self._handle_patient()
        elif user_type == "SA":
            self._handle_system_administrator()

    # TODO: add those methods
    def _handle_practitioner(self):
        pass

    def _handle_family_member(self):
        pass

    def _handle_patient(self):
        pass

    def _handle_system_administrator(self):
        pass
