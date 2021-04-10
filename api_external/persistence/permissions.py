from django.contrib.auth.models import Group
from rest_framework import permissions

from persistence.enums.user_type_enums import UserType


def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PractitionerPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, UserType.PRACTITIONER.name)

    def has_object_permission(self, request, view, obj):
        return obj.assigned_practitioner.id == request.user.id


class FamilyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, UserType.FAMILY_MEMBER.name)

    def has_object_permission(self, request, view, obj):
        return request.user.id in obj.family_members


class PatientPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, UserType.PATIENT.name)

    def has_object_permission(self, request, view, obj):
        return obj.patient_account.id == request.user.id


class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_in_group(request.user, UserType.SYSTEM_ADMINISTRATOR.name)

    def has_object_permission(self, request, view, obj):
        return True
