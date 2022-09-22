from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='mainapp/')),
    path("mainapp/", include("mainapp.urls")),
    path("admin/", admin.site.urls),
]
