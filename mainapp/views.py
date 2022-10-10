import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View,
)

from .models import News, Courses, Lessons, Teachers, CourseFeedback
from .forms import CourseFeedbackForm, MailFeedbackForm
from .tasks import send_feedback_mail


logger = logging.getLogger(__name__)


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


class CoursesListView(ListView):
    model = Courses
    paginate_by = 3
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class CoursesDetailPageView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        logger.debug('Yet another log message')

        context = super().get_context_data(**kwargs)
        context['course_object'] = get_object_or_404(Courses, pk=pk)
        context['lessons'] = Lessons.objects.filter(course=context['course_object'])
        context['teachers'] = Teachers.objects.filter(course=context['course_object'])
        if not self.request.user.is_anonymous:
            if not CourseFeedback.objects.filter(
                    course=context['course_object'],
                    user=self.request.user
            ).count():
                context['feedback_form'] = CourseFeedbackForm(
                    course=context['course_object'],
                    user=self.request.user
                )

        cached_feedback = cache.get(f'feedback_list_{pk}')
        if not cached_feedback:
            context['feedback_list'] = CourseFeedback.objects.filter(
                course=context['course_object']
            ).order_by('-create_date', '-rating')[:5]

            cache.set(f'feedback_list_{pk}', context['feedback_list'], timeout=300)

            # Archive object for tests --->
            import pickle
            with open(
                    f'mainapp/fixtures/006_feedback_list_{pk}.bin', 'wb'
            ) as outf:
                pickle.dump(context['feedback_list'], outf)
            # <--- Archive object for tests

        else:
            context['feedback_list'] = cached_feedback

        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_card})


class LogView(TemplateView):
    template_name = 'mainapp/log_view.html'

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, 'r') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000: # first 1000 lines
                    break
                log_slice.insert(0, line) # append at start
            context['log'] = ''.join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))


class ContactsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'
    def get_context_data(self, **kwargs):
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = MailFeedbackForm(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(f'mail_feedback_lock_{self.request.user.pk}')
            if not cache_lock_flag:
                cache.set(
                    f'mail_feedback_lock_{self.request.user.pk}',
                    'lock',
                    timeout=300,
                )
                messages.add_message(self.request, messages.INFO, _('Message sended'))
                send_feedback_mail.delay(
                    {
                        'user_id': self.request.POST.get('user_id'),
                        'message': self.request.POST.get('message'),
                    }
                )
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _('You can send only one message per 5 minutes'),
                )
        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))
