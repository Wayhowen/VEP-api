from django.contrib.auth.models import Group
from django.core import exceptions
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from persistence.enums import UserType
from persistence.models import CustomUser, Patient


# TODO: https://www.django-rest-framework.org/api-guide/generic-views/
# TODO: User should belong to one group only, check how to make it work properly
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    patient_id = serializers.SerializerMethodField(read_only=True)
    assigned_practitioner_id = serializers.IntegerField(required=False)
    assigned_practitioner = serializers.SerializerMethodField(read_only=True)
    user_type = serializers.ModelField(model_field=CustomUser()._meta.get_field('type'))

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone_number', 'password', 'user_type', 'family_members',
                  'patient_id', 'assigned_practitioner_id', 'assigned_practitioner',
                  'assigned_patients')
        extra_kwargs = {
            'id': {'read_only': True},
            "user_type": {"default": "PT"},
            "assigned_patients": {"required": False, "many": True},
            "family_members": {"required": False},
            "patient": {"read_only": True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        try:
            group = Group.objects.get(name=UserType.get_name(validated_data['user_type']))
        except exceptions.ObjectDoesNotExist:
            group = Group.objects.get(name="PATIENT")

        user.groups.add(group)


        self._create_patient_if_pt(user, validated_data.get("assigned_practitioner_id"))
        self._assign_practitioner_to_patients_if_pr_or_pt(user,
                                                          validated_data.get("assigned_practitioner_id"))
        return user

    def _create_patient_if_pt(self, user, assigned_practitioner_id):
        if user.type == "PT":
            if assigned_practitioner_id:
                assigned_practitioner = get_object_or_404(CustomUser, id=assigned_practitioner_id)
                if assigned_practitioner.type == "PR":
                    patient = Patient.objects.create(patient_account=user,
                                                     assigned_practitioner_id=assigned_practitioner_id)
                else:
                    raise serializers.ValidationError({"Error": "Selected practitioner is not a practitioner"})
            else:
                raise serializers.ValidationError({"Error": "No Practitioner assigned for this user"})
            return patient

    def _assign_practitioner_to_patients_if_pr_or_pt(self, user, assigned_practitioner_id):
        if user.type == "PR":
            for patient in user.assigned_patients.all():
                patient.assigned_practitioner = user
        elif user.type == "PT":
            user.patient.assigned_practitioner = assigned_practitioner_id
        return user

    def get_patient_id(self, instance):
        if instance.type == "PT":
            return instance.patient.get().id
        return None

    def get_assigned_practitioner(self, instance):
        if instance.type == "PT":
            return instance.patient.get().assigned_practitioner.id
        return None


# TODO: could be updated so that users are not left without practitioners etc.
class UserUpdateDeleteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    patient_id = serializers.SerializerMethodField(read_only=True)
    assigned_practitioner_id = serializers.IntegerField(required=False)
    assigned_practitioner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone_number', 'password', 'family_members', 'patient_id',
                  'assigned_practitioner_id', 'assigned_practitioner', 'assigned_patients')
        extra_kwargs = {
            'id': {'read_only': True},
            "user_type": {"default": "PT"},
            "assigned_patients": {"required": False, "many": True},
            "family_members": {"required": False},
            "phone_number": {"required": False},
            "email": {"required": False},
        }

    def update(self, instance, validated_data):
        if relatives := validated_data.pop('family_members', None):
            if instance.type == "PT" or instance.type == "FM":
                instance.relatives.clear()
                for relative in relatives:
                    if instance.type == "PT" and relative.patient_account.type == "FM" or \
                            instance.type == "FM" and relative.patient_account.type == "PT":
                        instance.relatives.add(relative)
            else:
                raise serializers.ValidationError(
                    {"Error": "Adding relatives only possible for 'PT' or 'FM'"})
        if assigned_patients := validated_data.pop('assigned_patients', None):
            if instance.type == "PR":
                instance.assigned_patients.clear()
                for patient in assigned_patients:
                    if patient.patient_account.type == "PT":
                        instance.assigned_patients.add(patient)
            else:
                raise serializers.ValidationError(
                    {"Error": "Adding patients only possible for 'PR'"})

        instance.update(validated_data)
        return instance

    def get_patient_id(self, instance):
        if instance.type == "PT":
            return instance.patient.get().id
        return None

    def get_assigned_practitioner(self, instance):
        if instance.type == "PT":
            return instance.patient.get().assigned_practitioner.id
        return None
