from rest_framework import serializers

from api_ext.serializers.raw_recording_serializer import RawRecordingSerializer
from persistence.models import ActivityResult


class ActivityCreateResultSerializer(serializers.ModelSerializer):
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
        if validated_data["patient"].patient_account.type == "PT":
            activity_result = ActivityResult.objects.create(**validated_data)
            return activity_result
        raise serializers.ValidationError({"Error": "Data must be assigned to patient account"})


class ActivityGetUpdateDeleteSerializer(serializers.ModelSerializer):
    raw_recording = RawRecordingSerializer(many=False)

    class Meta:
        model = ActivityResult
        fields = "__all__"
        extra_kwargs = {"file": {"read_only": True}}

    def update(self, instance, validated_data):
        if patient := validated_data["patient"]:
            if patient.patient_account.type != "PT":
                raise serializers.ValidationError(
                    {"Error": "Data must be assigned to patient account"})

        if raw_recording_data := validated_data.pop("raw_recording", None):
            nested_serializer = self.fields["raw_recording"]
            nested_instance = instance.raw_recording
            nested_serializer.update(nested_instance, raw_recording_data)
        instance.update(validated_data)
        return instance
