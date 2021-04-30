from rest_framework import serializers

from persistence.models.job import Job


class JobCreateSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(source='patient.id')

    class Meta:
        model = Job
        fields = ('type', 'uid', 'status', 'patient_id', 'activity_result')
        read_only_fields = ('uid', 'status', 'start_datetime', 'finish_datetime', 'error_message')
        ref_name = "Job"

    def create(self, validated_data):
        validated_data["job_type"] = validated_data.pop("type")
        job = Job.objects.create_new(**validated_data)
        return job


class JobGetUpdateSerializer(serializers.ModelSerializer):
    partial = True

    class Meta:
        model = Job
        fields = ('uid', 'status', 'start_datetime', 'finish_datetime', 'error_message',
                  'patient_id', 'activity_result_id')
        read_only_fields = ('uid', 'patient_id', 'activity_result_id')
        extra_kwargs = {
            'status': {'required': False},
            'start_datetime': {'required': False},
            'finish_datetime': {'required': False}
        }
        ref_name = "Job"

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance
