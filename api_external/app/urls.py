import os

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]

if os.environ.get('API_EXT_ENABLED') == 'true':
    urlpatterns.append(path('api/', include('api_ext.urls')))
