from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from mainapp.apps import MainappConfig
from authapp.apps import AuthappConfig

urlpatterns = [
    path('', RedirectView.as_view(url='mainapp/')),
    path('admin/', admin.site.urls),
    path('mainapp/', include('mainapp.urls', namespace=MainappConfig.name)),
    path('authapp/', include('authapp.urls', namespace=AuthappConfig.name)),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
