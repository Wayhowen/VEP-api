from rest_framework import serializers

from api_ext.serializers.utils.fuzzy_set_validator import FuzzyValidator
from persistence.models.ai_config_models.fuzzy_setup import FuzzySetup


class FuzzySetupCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FuzzySetup
        fields = "__all__"
        read_only_fields = ('id', )
        extra_kwargs = {
            'patient': {'required': True},
        }
        ref_name = "Fuzzy Setup"

    # TODO: might add rules validation by regex later
    def validate_rules(self, data):
        validator = FuzzyValidator()
        return validator.validate_rules(data)

    def validate_patient(self, data):
        validator = FuzzyValidator()
        return validator.validate_patient(data)

    def validate_universes_description(self, data):
        validator = FuzzyValidator()
        validator.validate_universes(data)
        return data


class FuzzySetupGetUpdateDeleteSerializer(serializers.ModelSerializer):
    partial = True

    class Meta:
        model = FuzzySetup
        fields = "__all__"
        read_only_fields = ('id', )
        extra_kwargs = {
            'patient': {'read_only': True, 'required': False},
            'rules': {'required': False},
            'universes_description': {'required': False}
        }
        ref_name = "Fuzzy Setup"

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance

    def validate_rules(self, data):
        validator = FuzzyValidator()
        return validator.validate_rules(data)

    def validate_patient(self, data):
        validator = FuzzyValidator()
        return validator.validate_patient(data)

    def validate_universes_description(self, data):
        validator = FuzzyValidator()
        validator.validate_universes(data)
        return data
