from datetime import datetime

from django.views.generic import TemplateView


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_title'] = 'Новость'
        context['news_descripton'] = 'Предваритеьно описание новости'
        context['news_date'] = datetime.now()
        context['range'] = range(5)
        return context


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"
