from django.contrib.auth.models import Group
from django.core import exceptions
from rest_framework import serializers

from persistence.enums import UserType
from persistence.models import CustomUser


# TODO: https://www.django-rest-framework.org/api-guide/generic-views/
# TODO: User should belong to one group only, check how to make it work properly
class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password', 'type')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        try:
            group = Group.objects.get(name=UserType.get_name(validated_data['type']))
        except exceptions.ObjectDoesNotExist:
            group = Group.objects.get(name="PATIENT")
        user.groups.add(group)
        return user

    def update(self, instance, validated_data):
        user_type = validated_data.get('type', None)
        if user_type:
            instance.groups.clear()
            try:
                group = Group.objects.get(name=UserType.get_name(user_type))
            except Exception as e:
                raise serializers.ValidationError(
                    {"Missing Group": f"There is no group called '{user_type}'"})

            instance.groups.add(group)
        instance.update(validated_data)
        return instance
