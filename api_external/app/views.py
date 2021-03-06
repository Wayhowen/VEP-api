import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import CustomUser
from app.permissions import PractitionerPermissions, FamilyPermissions, PatientPermissions, \
    AdminPermissions
from app.serializers import UserSerializer


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
        user = CustomUser.objects.filter(email=request.data['email'])[0]
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
