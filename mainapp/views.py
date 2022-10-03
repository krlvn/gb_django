from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import News, Courses, Lessons, Teachers


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class NewsListView(ListView):
    model = News
    paginate_by = 5
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsDetailView(DetailView):
    model = News


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


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
