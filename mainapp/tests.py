import pickle
from unittest import mock
from http import HTTPStatus

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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


class TestNewsSelenium(StaticLiveServerTestCase):
    fixtures = (
        'authapp/fixtures/001_user_admin.json',
        'mainapp/fixtures/001_news.json',
    )

    def setUp(self):
        super().setUp()
        self.selenium = WebDriver(executable_path=settings.SELENIUM_DRIVER_PATH_FF)
        self.selenium.implicitly_wait(10)
        # Login
        self.selenium.get(f'''{self.live_server_url}{reverse('authapp:login')}''')
        button_enter = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[type="submit"]'))
        )
        self.selenium.find_element(By.ID, 'id_username').send_keys('admin')
        self.selenium.find_element(By.ID, 'id_password').send_keys('admin')
        button_enter.click()
        # Wait for footer
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'mt-auto'))
        )

    def test_create_button_clickable(self):
        path_list = f'''{self.live_server_url}{reverse('mainapp:news')}'''
        path_add = reverse('mainapp:news_create')
        self.selenium.get(path_list)
        button_create = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f'[href="{path_add}"]')
            )
        )
        print('Trying to click button ...')
        button_create.click()
        WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.ID, 'id_title'))
        )
        print('Button clickable!')


    def test_pick_color(self):
        path = f'''{self.live_server_url}{reverse('mainapp:main')}'''
        self.selenium.get(path)
        navbar_el = WebDriverWait(self.selenium, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'navbar'))
        )
        try:
            self.assertEqual(navbar_el.value_of_css_property('background-color'), 'rgb(255, 255, 155)')
        except AssertionError:
            with open('var/screenshots/001_navbar_el_scrnsht.png', 'wb') as outf:
                outf.write(navbar_el.screenshot_as_png)
            raise

        def tearDown(self):
            # Close browser
            self.selenium.quit()
            super().tearDown()
