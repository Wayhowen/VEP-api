from rest_framework import serializers

from persistence.models.job import Job


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('type', 'uid', 'status')
        read_only_fields = ('uid', 'status')
        ref_name = "Job"

    def create(self, validated_data):
        job = Job.objects.create_new(**validated_data)
        return job


class JobGetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('uid', 'status', 'start_datetime', 'finish_datetime')
        read_only_fields = ('uid', )
        extra_kwargs = {
            'status': {'required': False},
            'start_datetime': {'required': False},
            'finish_datetime': {'required': False}
        }
        ref_name = "Job"

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance
