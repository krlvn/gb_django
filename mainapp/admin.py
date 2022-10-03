from django.contrib import admin

from mainapp import models as mainapp_models

@admin.register(mainapp_models.News)
class NewsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'preambule', 'body']
