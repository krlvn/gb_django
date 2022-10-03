from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from authapp import models as authapp_models
@admin.register(authapp_models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'date_joined']
    ordering = ['-date_joined']
