import debug_toolbar

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from mainapp.apps import MainappConfig
from authapp.apps import AuthappConfig

urlpatterns = [
    path('', RedirectView.as_view(url='mainapp/')),
    path('i18n/', include('django.conf.urls.i18n'), name='set_language'),
    path('social_auth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('mainapp/', include('mainapp.urls', namespace=MainappConfig.name)),
    path('authapp/', include('authapp.urls', namespace=AuthappConfig.name)),
]

if settings.DEBUG:
   urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
