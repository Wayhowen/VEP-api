import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]

if os.environ.get('API_EXT_ENABLED') == 'true':
    urlpatterns.append(path('api/', include('api_ext.urls')))
if os.environ.get('CHARTS_ENABLED') == 'true':
    urlpatterns.append(path('graphs/', include('chartjs.urls')))

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
