from rest_framework import serializers

from api_ext.serializers.raw_recording_serializer import RawRecordingSerializer
from persistence.models import ActivityResult


class ActivityResultSerializer(serializers.ModelSerializer):
    raw_recording = RawRecordingSerializer(many=False)

    class Meta:
        model = ActivityResult
        fields = "__all__"

    def create(self, validated_data):
        raw_recording_serializer = RawRecordingSerializer(data=validated_data.pop("raw_recording"))
        if raw_recording_serializer.is_valid():
            raw_recording_serializer.save()
        raw_recording = raw_recording_serializer.instance
        validated_data["raw_recording_id"] = raw_recording.id
        ar = ActivityResult.objects.create(**validated_data)
        return ar
