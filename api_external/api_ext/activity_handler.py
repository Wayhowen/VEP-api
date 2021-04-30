from django.shortcuts import get_list_or_404
from rest_framework.request import Request

from persistence.models import ActivityResult, RawRecording


class Handler:
    def __init__(self):
        pass

    def process(self, request: Request) -> dict:
        dict_query = dict(request.data)

        if patient_email := dict_query.get("patient_email", None):
            raw_recording_ids = ActivityResult.objects.filter(
                patient__patient_account__email=patient_email).values_list('raw_recording',
                                                                           flat=True)
        elif patient_id := dict_query.get("patient_id", None):
            raw_recording_ids = ActivityResult.objects.filter(
                patient__id=patient_id).values_list('raw_recording', flat=True)
        elif activity_id := dict_query.get("activity_id", None):
            raw_recording_ids = ActivityResult.objects.filter(
                id=activity_id).values_list('raw_recording', flat=True)
        else:
            raw_recording_ids = []
        query = RawRecording.objects.filter(id__in=raw_recording_ids).order_by('-id')

        if "activity_name" in dict_query:
            query = query.filter(name=dict_query["activity_name"])
        if "timestamp_from" in dict_query:
            query = query.filter(start_time__gte=dict_query["timestamp_from"])
        if "timestamp_to" in dict_query:
            query = query.filter(start_time__lte=dict_query["timestamp_to"])
        response_data = {"raw_recordings": self._create_response_dicts_list(get_list_or_404(query))}
        return response_data

    def _create_response_dicts_list(self, objects):
        response_dicts_list = []
        for activity in objects:
            activity_dict = dict()
            activity_dict[activity.name] = {
                "id": activity.id,
                "start_timestamp": activity.start_time,
                "finish_timestamp": activity.finish_time,
                "file_url": activity.file.creation_url
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
