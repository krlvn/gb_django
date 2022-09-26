from datetime import datetime
from django.core.paginator import Paginator
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