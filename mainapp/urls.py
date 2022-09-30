from django.urls import path

from .views import *
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('doc_site/', DocSitePageView.as_view(), name='doc_site'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('news/', NewsPageView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailPageView.as_view(), name='news_detail'),
    path('courses/', CoursesPageView.as_view(), name='courses'),
    path('courses/<int:pk>/', CoursesDetailPageView.as_view(), name='courses_detail'),
]
