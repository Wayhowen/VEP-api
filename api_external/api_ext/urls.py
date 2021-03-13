from django.urls import path, include

from api_ext import views

urlpatterns = [
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('ping/', views.ping),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.UserAPIView.as_view(), name='users'),
    path('practitioner/', views.practitioner_view),
    path('job/', views.JobAPIView.as_view(), name='job'),
    path('job/<str:uid>', views.JobAPIView.as_view(), name='job_details')
]
