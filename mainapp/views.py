from django.views.generic import TemplateView

class MainPageView(TemplateView):
    template_name = 'index.html'

class LoginPageView(TemplateView):
    template_name = 'login.html'

class DocSitePageView(TemplateView):
    template_name = 'doc_site.html'

class ContactsPageView(TemplateView):
    template_name = 'contacts.html'

class NewsPageView(TemplateView):
    template_name = 'news.html'

class CoursesPageView(TemplateView):
    template_name = 'courses_list.html'
