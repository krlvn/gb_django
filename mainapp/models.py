from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from mainapp.managers.news_manager import NewsManager
from mainapp.managers.courses_manager import CoursesManager
from mainapp.managers.lessons_manager import LessonsManager
from mainapp.managers.teachers_manager import TeachersManager

class News(models.Model):
    objects = NewsManager()

    title = models.CharField(max_length=256, verbose_name='Title')
    preambule = models.CharField(max_length=1024, blank=True, null=True, verbose_name='Preambule')
    body = models.TextField(blank=False, null=False, verbose_name='Body')
    body_as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Date of creating', editable=False)
    update_date = models.DateTimeField(auto_now=True, verbose_name='Date of editing', editable=False)
    deleted = models.BooleanField(default=False)

    class Meta():
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ('-create_date',)

    def __str__(self):
        return f'{self.pk} {self.title}'

    def delete(self, *args):
        self.deleted = True
        self.save()


class Courses(models.Model):
    objects = CoursesManager()

    name = models.CharField(max_length=256, verbose_name='Name')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    description_as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Cost')
    cover = models.CharField(max_length=25, default='no_image.svg', verbose_name='Cover')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Date of creating', editable=False)
    update_date = models.DateTimeField(auto_now=True, verbose_name='Date of editing', editable=False)
    deleted = models.BooleanField(default=False)

    class Meta():
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ('-create_date',)

    def __str__(self):
        return f'{self.pk} {self.name}'

    def delete(self, *args):
        self.deleted = True
        self.save()


class Lessons(models.Model):
    objects = LessonsManager()

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name='Lesson number')
    title = models.CharField(max_length=256, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    description_as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Date of creating', editable=False)
    update_date = models.DateTimeField(auto_now=True, verbose_name='Date of editing', editable=False)
    deleted = models.BooleanField(default=False)

    class Meta():
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ('course', 'num',)

    def __str__(self):
        return f'{self.course.name} | {self.num} | {self.title}'

    def delete(self, *args):
        self.deleted = True
        self.save()


class Teachers(models.Model):
    objects = TeachersManager()

    course = models.ManyToManyField(Courses)
    name = models.CharField(max_length=128, verbose_name='Name')
    surname = models.CharField(max_length=128, verbose_name='Surname')
    birth_date = models.DateField(verbose_name='Birth date')
    deleted = models.BooleanField(default=False)

    class Meta():
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        ordering = ('name', 'surname',)

    def __str__(self):
        return f'{self.pk} | {self.name} {self.surname}'

    def delete(self, *args):
        self.deleted = True
        self.save()


class CourseFeedback(models.Model):
    RATING = (
        (5, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (3, '⭐⭐⭐'),
        (2, '⭐⭐'),
        (1, '⭐')
    )

    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name=_('Course'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('User'))
    feedback = models.TextField(default=_('No feedback'), verbose_name=_('Feedback'))
    rating = models.SmallIntegerField(choices=RATING, default=5, verbose_name=_('Rating'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Date of creating', editable=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.course} ({self.user})'
