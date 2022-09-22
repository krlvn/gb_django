from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from mainapp.apps import MainappConfig

urlpatterns = [
    path('', RedirectView.as_view(url='mainapp/')),
    path('mainapp/', include('mainapp.urls', namespace=MainappConfig.name)),
    path('admin/', admin.site.urls),
]
