import json

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from api_ext.serializers.job_serializer import JobCreateSerializer, JobGetUpdateSerializer
from persistence.models import CustomUser
from persistence.models.job import Job
from persistence.permissions import PractitionerPermissions, FamilyPermissions, PatientPermissions, \
    AdminPermissions
from api_ext.serializers import UserSerializer
from tasks.celeryapp import app as celery_app


def ping(request):
    return HttpResponse('external pong')


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_view(request):
    data_unicode = request.body.decode('utf-8')
    data = json.loads(data_unicode)
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)
    user = authenticate(request, username=username, email=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse()
    return HttpResponse(status=401)


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return HttpResponse()


@authentication_classes([])
@permission_classes([])
class UserAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(serializer.data)

    def put(self, request):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
        except ObjectDoesNotExist:
            return Response(status=404,
                            data={"error": f"User with email='{request.data['email']}' not found."})
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes((PractitionerPermissions, ))
def practitioner_view(request):
    return HttpResponse()


@permission_classes((FamilyPermissions, ))
@api_view(['GET'])
def family_view(request):
    return HttpResponse()


@permission_classes((PatientPermissions, ))
@api_view(['GET'])
def patient_view(request):
    return HttpResponse()


@permission_classes((AdminPermissions, ))
@api_view(['GET'])
def admin_view(request):
    return HttpResponse()


@permission_classes([HasAPIKey | AdminPermissions | PractitionerPermissions])
class JobAPIView(APIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateSerializer
        return JobGetUpdateSerializer

    def get(self, request, uid):
        job = Job.objects.get_and_update(uid, ['last_edited_datetime'])
        serializer = self.get_serializer_class()(job)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            celery_app.send_task('process_data', (serializer.instance.uid, serializer.instance.type, ))
        else:
            return Response(serializer.errors)
        return Response(serializer.data)

    def put(self, request, uid):
        print(request.data)
        try:
            job = Job.objects.get_and_update(uid, ['last_edited_datetime'])
        except ObjectDoesNotExist:
            return Response(status=404,
                            data={"error": f"Job with uid='{uid}' not found."})
        serializer = self.get_serializer_class()(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(serializer.data)

