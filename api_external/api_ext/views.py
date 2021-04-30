import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from api_ext.serializers.job_serializers import JobCreateSerializer, JobGetUpdateSerializer
from persistence.models import CustomUser, Job, Patient, ActivityResult
from persistence.models.ai_config_models.fuzzy_setup import FuzzySetup
from persistence.permissions import PractitionerPermissions, FamilyPermissions, \
    PatientPermissions, AdminPermissions
from tasks.celeryapp import app as celery_app
from .activity_handler import Handler as ActivityHandler
from .custom_parser import MultipartJsonParser
from .serializers.activity_result_serializers import ActivityCreateResultSerializer, \
    ActivityGetUpdateDeleteSerializer
from .serializers.fuzzy_setup_serializer import FuzzySetupCreateSerializer, \
    FuzzySetupGetUpdateDeleteSerializer
from .serializers.patient_serializer import PatientSerializer
from .serializers.user_serializer import UserUpdateDeleteSerializer, UserCreateSerializer


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
class UserCreateAPIView(APIView):
    """
    Endpoint for managing user auth objects.

    post:
    Creating users

    put:
    Editing users
    """
    serializer_class = UserCreateSerializer

    # docs response says it returns password but it doesn't - see:
    # https://github.com/axnsan12/drf-yasg/issues/70
    @swagger_auto_schema(request_body=UserCreateSerializer(many=False),
                         responses={200: UserCreateSerializer(many=False)},
                         tags=["Users"], operation_description="Endpoint for creating users.")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


@permission_classes([AdminPermissions | PractitionerPermissions])
class UserUpdateAPIView(APIView):
    serializer_class = UserUpdateDeleteSerializer

    @swagger_auto_schema(request_body=UserUpdateDeleteSerializer(many=False),
                         responses={200: UserUpdateDeleteSerializer(many=False)},
                         tags=["Users"], operation_description="Endpoint for updating users data.")
    def put(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: "User instance sucessfully deleted"},
                         tags=["Users"], operation_description="Endpoint for deleting users.")
    def delete(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        user.delete()
        return Response(status=200)


@permission_classes([HasAPIKey | AdminPermissions | PractitionerPermissions])
class CreateJobAPIView(APIView):
    serializer_class = JobCreateSerializer
    """
    Endpoint responsible for creating jobs.
    """

    @swagger_auto_schema(request_body=JobCreateSerializer(many=False),
                         responses={200: JobCreateSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
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
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions"),
                                    404: openapi.Response("Object does not exist")},
                         tags=["Job"], operation_description="Get details about a job object.")
    def get(self, request, uid):
        job = get_object_or_404(Job, uid=uid)
        serializer = self.serializer_class(job)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: JobGetUpdateSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions"),
                                    404: openapi.Response("Object does not exist")},
                         tags=["Job"],
                         operation_description="Update job object. Endpoint meant for workers only"
                                               " and should not be used by users.")
    def put(self, request, uid):
        job = get_object_or_404(Job, uid=uid)
        serializer = self.serializer_class(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@swagger_auto_schema(method='post',
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         required=['email', ],
                         properties={
                             'patient_email': openapi.Schema(
                                 title="Patient for whom the data is aggregated",
                                 type=openapi.TYPE_STRING,
                                 max_length="256",
                                 format="email"),
                             'patient_id': openapi.Schema(
                                 title="The ID of the patient for whom to return the data\n"
                                       "Exchangeable with patient_email",
                                 type=openapi.TYPE_INTEGER),
                             'activity_id': openapi.Schema(
                                 title="The ID of ActivityResult for which to return the data",
                                 type=openapi.TYPE_INTEGER),
                             'activity_name': openapi.Schema(title="Name of requested activity",
                                                             type=openapi.TYPE_STRING,
                                                             max_length="256",
                                                             enum=["Walk 40 seconds"]),
                             'timestamp_from': openapi.Schema(
                                 title="Starting timestamp for DB query",
                                 type=openapi.TYPE_INTEGER),
                             # format="YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"),
                             'timestamp_to': openapi.Schema(title="Final timestamp for DB query",
                                                            type=openapi.TYPE_INTEGER)
                             # format="YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
                         }),
                     responses={
                         200: openapi.Response("Query returned some data"),
                         401: openapi.Response(
                             "User not logged in or do not have permission for data requested"),
                         404: openapi.Response("Query did not find any data"),
                     },
                     tags=['Data Management'],
                     operation_description="Endpoint for getting raw activity data for activities"
                                           " done by users",
                     operation_id="activity_result_list",
                     )
@api_view(['POST'])
@permission_classes([HasAPIKey | AdminPermissions | PractitionerPermissions | PatientPermissions |
                     FamilyPermissions])
def activity_result_aggregation_view(request):
    data_handler = ActivityHandler()
    response_data = data_handler.process(request)
    return Response(data=response_data)


class ActivityCreateAPIView(APIView):
    parser_classes = (MultipartJsonParser, JSONParser)
    serializer_class = ActivityCreateResultSerializer

    @swagger_auto_schema(request_body=ActivityCreateResultSerializer(many=False),
                         responses={200: ActivityCreateResultSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Data Management"],
                         operation_description="Endpoint for inserting activity data.\n"
                                               "In the body, there should be another parameter with"
                                               " key 'file' and a value of a zipped raw activity"
                                               " data.\nThis endpoint should be requested with"
                                               " multipart/form request type.")
    def post(self, request):
        file_obj = request.FILES['file']

        request.data['raw_recording']['file'] = file_obj
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(data=serializer.errors)


@permission_classes([])
class ActivityGetUpdateDeleteAPIView(APIView):
    serializer_class = ActivityGetUpdateDeleteSerializer

    @swagger_auto_schema(responses={200: ActivityGetUpdateDeleteSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Data Management"],
                         operation_description="Endpoint for getting activity data")
    def get(self, request, activity_id):
        activity_result = get_object_or_404(ActivityResult, id=activity_id)
        serializer = self.serializer_class(activity_result)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ActivityGetUpdateDeleteSerializer(many=False),
                         responses={200: ActivityGetUpdateDeleteSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Data Management"],
                         operation_description="Endpoint for updating activity data")
    def put(self, request, activity_id):
        activity_result = get_object_or_404(ActivityResult, id=activity_id)
        serializer = self.serializer_class(activity_result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @swagger_auto_schema(responses={200: "Object sucessfully deleted",
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Data Management"],
                         operation_description="Endpoint for removing activity data")
    def delete(self, request, activity_id):
        activity_result = get_object_or_404(ActivityResult, id=activity_id)
        activity_result.delete()
        return Response(status=200)


@permission_classes([HasAPIKey | AdminPermissions | PractitionerPermissions
                     | PatientPermissions | FamilyPermissions | AdminPermissions])
class PatientAPIView(APIView):
    serializer_class = PatientSerializer

    @swagger_auto_schema(responses={200: PatientSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Users"],
                         operation_description="Endpoint for getting patient data")
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, pk=patient_id)
        self.check_object_permissions(request, patient)
        serializer = self.serializer_class(patient)
        return Response(serializer.data)


@permission_classes([AdminPermissions | PractitionerPermissions])
class FuzzySetupCreateAPIView(APIView):
    serializer_class = FuzzySetupCreateSerializer

    @swagger_auto_schema(request_body=FuzzySetupCreateSerializer(many=False),
                         responses={200: FuzzySetupCreateSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Fuzzy Logic Setup"],
                         operation_description="Endpoint for creating fuzzy setup data")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)


@permission_classes([AdminPermissions | PractitionerPermissions | HasAPIKey])
class FuzzySetupGetUpdateDeleteAPIView(APIView):
    serializer_class = FuzzySetupGetUpdateDeleteSerializer

    @swagger_auto_schema(responses={200: FuzzySetupGetUpdateDeleteSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Fuzzy Logic Setup"],
                         operation_description="Endpoint for getting fuzzy setup data")
    def get(self, request, patient_id):
        fuzzy_setup = FuzzySetup.objects.filter(patient_id=patient_id)
        if not fuzzy_setup.exists():
            fuzzy_setup = FuzzySetup.objects.get(patient_id=None)
        else:
            fuzzy_setup = fuzzy_setup.get()
            self.check_object_permissions(request, fuzzy_setup)
        serializer = self.serializer_class(fuzzy_setup)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=FuzzySetupGetUpdateDeleteSerializer(many=False),
                         responses={200: FuzzySetupGetUpdateDeleteSerializer(many=False),
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Fuzzy Logic Setup"],
                         operation_description="Endpoint for updating fuzzy setup data")
    def put(self, request, patient_id):
        fuzzy_setup = get_object_or_404(FuzzySetup, patient_id=patient_id)
        self.check_object_permissions(request, fuzzy_setup)
        serializer = self.serializer_class(fuzzy_setup, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @swagger_auto_schema(responses={200: "Instance successfully deleted",
                                    403: openapi.Response(
                                        "User not logged in or does not have correct permissions")},
                         tags=["Fuzzy Logic Setup"],
                         operation_description="Endpoint for deleting fuzzy setup instances")
    def delete(self, request, patient_id):
        fuzzy_setup = get_object_or_404(FuzzySetup, patient_id=patient_id)
        fuzzy_setup.delete()
        return Response(status=200)
