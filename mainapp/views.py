from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import News, Courses, Lessons, Teachers


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    paginated_by = 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(News.objects.all(), self.paginated_by)
        page = paginator.get_page(page_number)
        context['page'] = page

        return context

class NewsDetailPageView(TemplateView):
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_object'] = get_object_or_404(News, pk=pk)
        return context


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"

    paginated_by = 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(Courses.objects.all(), self.paginated_by)
        page = paginator.get_page(page_number)
        context['page'] = page

        return context


class CoursesDetailPageView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_object'] = get_object_or_404(Courses, pk=pk)
        context['lessons'] = Lessons.objects.filter(course=context['course_object'])
        context['teachers'] = Teachers.objects.filter(course=context['course_object'])
        return context
