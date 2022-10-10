import pickle
from unittest import mock

from http import HTTPStatus
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse

from .models import News, Courses
from authapp.models import CustomUser
from .tasks import send_feedback_mail

class TestMainPage(TestCase):
    def test_page_open(self):
        path = reverse('mainapp:main')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class TestNewsPageWithAuth(TestCase):
    fixtures = (
        'authapp/fixtures/001_user_admin.json',
        'mainapp/fixtures/001_news.json',
    )

    def setUp(self):
        super().setUp()
        self.client_with_auth = Client()
        path_auth = reverse('authapp:login')
        self.client_with_auth.post(
            path_auth,
            {'username': 'admin', 'password': 'admin'}
        )

    def test_open_page_create(self):
        path = reverse('mainapp:news_create')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create(self):
        counter_before = News.objects.count()
        path = reverse('mainapp:news_create')
        self.client_with_auth.post(
            path,
            {
                'title': 'Тest news title',
                'preambule': 'Test news preambule',
                'body': 'Test news body',
            },
        )
        self.assertGreater(News.objects.count(), counter_before)

    def test_open_page_update(self):
        news_obj = News.objects.first()
        path = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_update(self):
        new_title = 'New title of news'
        news_obj = News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client_with_auth.post(
            path,
            {
                'title': new_title,
                'preambule': news_obj.preambule,
                'body': news_obj.body,
            },
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_open_page_delete(self):
        news_obj = News.objects.first()
        path = reverse('mainapp:news_delete', args=[news_obj.pk])
        result = self.client_with_auth.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete(self):
        news_obj = News.objects.first()
        path = reverse('mainapp:news_delete', args=[news_obj.pk])
        self.client_with_auth.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


class TestNewsPageNotAuth(TestCase):
    fixtures = (
        'mainapp/fixtures/001_news.json',
    )

    def test_open_page_create(self):
        path = reverse('mainapp:news_create')
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create(self):
        counter_before = News.objects.count()
        path = reverse('mainapp:news_create')
        self.client.post(
            path,
            {
                'title': 'Тest news title',
                'preambule': 'Test news preambule',
                'body': 'Test news body',
            },
        )
        self.assertGreater(News.objects.count(), counter_before)

    def test_open_page_update(self):
        news_obj = News.objects.first()
        path = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_update(self):
        new_title = 'New title of news'
        news_obj = News.objects.first()
        self.assertNotEqual(news_obj.title, new_title)
        path = reverse('mainapp:news_update', args=[news_obj.pk])
        result = self.client.post(
            path,
            {
                'title': new_title,
                'preambule': news_obj.preambule,
                'body': news_obj.body,
            },
        )
        self.assertEqual(result.status_code, HTTPStatus.FOUND)
        news_obj.refresh_from_db()
        self.assertEqual(news_obj.title, new_title)

    def test_open_page_delete(self):
        news_obj = News.objects.first()
        path = reverse('mainapp:news_delete', args=[news_obj.pk])
        result = self.client.post(path)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_delete(self):
        news_obj = News.objects.first()
        path = reverse('mainapp:news_delete', args=[news_obj.pk])
        self.client.post(path)
        news_obj.refresh_from_db()
        self.assertTrue(news_obj.deleted)


class TestTaskMailSend(TestCase):
    fixtures = (
        'authapp/fixtures/001_user_admin.json',
    )

    def test_mail_send(self):
        message_text = 'Test message text'
        user_obj = CustomUser.objects.first()
        send_feedback_mail(
            {'user_id': user_obj.id, 'message': message_text}
        )
        self.assertEqual(mail.outbox[0].body, message_text)


class TestCoursesWithMock(TestCase):
    fixtures = (
        'authapp/fixtures/001_user_admin.json',
        'mainapp/fixtures/002_courses.json',
        'mainapp/fixtures/003_lessons.json',
        'mainapp/fixtures/004_teachers.json',
    )

    def test_page_open_detail(self):
        course_obj = Courses.objects.get(pk=2)
        path = reverse("mainapp:courses_detail", args=[course_obj.pk])
        with open('mainapp/fixtures/006_feedback_list_2.bin', 'rb') as inpf, \
            mock.patch('django.core.cache.cache.get') as mocked_cache:
            mocked_cache.return_value = pickle.load(inpf)
            result = self.client.get(path)
            self.assertEqual(result.status_code, HTTPStatus.OK)
            self.assertTrue(mocked_cache.called)
