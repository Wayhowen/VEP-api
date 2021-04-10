from django.conf.urls import url
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api_ext import views

schema_view = get_schema_view(
    openapi.Info(
        title="VEP API",
        default_version='v1',
        description="Test description",
        # TODO: ADD terms of service
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jas103@aber.ac.uk"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('ping/', views.ping),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.UserCreateAPIView.as_view(), name='users'),
    path('users/<int:user_id>', views.UserUpdateAPIView.as_view(), name='users_details'),
    path('practitioner/', views.practitioner_view),
    path('job/', views.CreateJobAPIView.as_view(), name='job'),
    path('job/<str:uid>', views.GetUpdateJobAPIView.as_view(), name='job_details'),
    path('raw_recording/', views.raw_recording_data_view, name='raw_recording'),
    path('activity/', views.ActivityAPIView.as_view(), name='activity'),
    path('patients/<int:patient_id>', views.PatientAPIView.as_view(), name='patients')
]
