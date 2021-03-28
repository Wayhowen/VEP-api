from rest_framework import serializers

from persistence.models.data_models.raw_recording import RawRecording


class RawRecordingSerializer(serializers.ModelSerializer):

    class Meta:
        model = RawRecording
        fields = ('name', 'start_time', 'finish_time', 'file')
