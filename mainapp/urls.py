from django.urls import path

from .views import *
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('doc_site/', DocSitePageView.as_view(), name='doc_site'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),

    path("news/", NewsListView.as_view(), name='news'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/update', NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),

    path('courses/', CoursesPageView.as_view(), name='courses'),
    path('courses/<int:pk>/', CoursesDetailPageView.as_view(), name='courses_detail'),
]
