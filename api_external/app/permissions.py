from django.contrib.auth.models import Group
from rest_framework import permissions

from app.enums.user_type_enums import UserType


def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class PractitionerPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, UserType.PRACTITIONER.name)


class FamilyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, UserType.FAMILY_MEMBER.name)


class PatientPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, UserType.PATIENT.name)


class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, UserType.SYSTEM_ADMINISTRATOR.name)
