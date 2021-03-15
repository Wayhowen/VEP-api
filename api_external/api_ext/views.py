import json

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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


@swagger_auto_schema(method='post',
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=['email', 'password'],
                         properties={
                             'email': openapi.Schema(title="User Email",
                                                     type=openapi.TYPE_STRING,
                                                     max_length="254",
                                                     min_length="1",
                                                     format="email"),
                             'password': openapi.Schema(title="User Password",
                                                        type=openapi.TYPE_STRING,
                                                        max_length="128",
                                                        min_length="1",
                                                        format="password")
                         }),
                     responses={
                         200: openapi.Response("Successful login"),
                         401: openapi.Response("Wrong credentials"),
                     },
                     tags=['Authentication and Authorization'],
                     operation_description="Endpoint for logging in."
                     )
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


@swagger_auto_schema(method='get',
                     responses={
                         200: openapi.Response("Successful logout"),
                         401: openapi.Response("User was not logged in"),
                     },
                     tags=['Authentication and Authorization'],
                     operation_description="Endpoint for logging out."
                     )
@api_view(['GET'])
def logout_view(request):
    logout(request)
    return HttpResponse()


@authentication_classes([])
@permission_classes([])
class UserAPIView(APIView):
    """
    Endpoint for managing user auth objects.

    post:
    Creating users

    put:
    Editing users
    """
    serializer_class = UserSerializer

    # TODO: docs response says it returns password but it doesn't - see:
    # https://github.com/axnsan12/drf-yasg/issues/70
    @swagger_auto_schema(request_body=UserSerializer(many=False),
                         responses={200: UserSerializer(many=False)},
                         tags=["Users"], )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer(many=False),
                         responses={200: UserSerializer(many=False)},
                         tags=["Users"], )
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
@permission_classes((PractitionerPermissions,))
def practitioner_view(request):
    return HttpResponse()


@permission_classes((FamilyPermissions,))
@api_view(['GET'])
def family_view(request):
    return HttpResponse()


@permission_classes((PatientPermissions,))
@api_view(['GET'])
def patient_view(request):
    return HttpResponse()


@permission_classes((AdminPermissions,))
@api_view(['GET'])
def admin_view(request):
    return HttpResponse()


@permission_classes([HasAPIKey | AdminPermissions | PractitionerPermissions])
class CreateJobAPIView(APIView):
    serializer_class = JobCreateSerializer
    """
    Endpoint responsible for creating jobs.
    """
    @swagger_auto_schema(request_body=JobCreateSerializer(many=False),
                         responses={200: JobCreateSerializer(many=False),
                                    403: openapi.Response("User not logged in or does not have correct permissions")},
                         tags=["Job"], operation_description="Endpoint for creating jobs.")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            celery_app.send_task('process_data',
                                 (serializer.instance.uid, serializer.instance.type,))
        else:
            return Response(serializer.errors)
        return Response(serializer.data)


@permission_classes([HasAPIKey | AdminPermissions | PractitionerPermissions])
class GetUpdateJobAPIView(APIView):
    serializer_class = JobGetUpdateSerializer
    """
    Endpoint Responsible for retrieving/updating job objects.
    """

    @swagger_auto_schema(responses={200: JobGetUpdateSerializer(many=False),
                                    403: openapi.Response("User not logged in or does not have correct permissions"),
                                    404: openapi.Response("Object does not exist")},
                         tags=["Job"], operation_description="Get details about a job object.")
    def get(self, request, uid):
        job = Job.objects.get_and_update(uid, ['last_edited_datetime'])
        serializer = self.serializer_class(job)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: JobGetUpdateSerializer(many=False),
                                    403: openapi.Response("User not logged in or does not have correct permissions"),
                                    404: openapi.Response("Object does not exist")},
                         tags=["Job"], operation_description="Update job object. Endpoint meant for workers only and should not be used by users.")
    def put(self, request, uid):
        job = Job.objects.get_and_update(uid, ['last_edited_datetime'])
        serializer = self.serializer_class(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(serializer.data)
