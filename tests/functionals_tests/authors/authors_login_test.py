import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def test_user_valid_data_can_login_successfulty(self):
        string_password = 'pass'

        user = User.objects.create_user(
            username='usertest', password=string_password)
        # user open browser in page login

        self.browser.get(self.live_server_url + reverse('authors:login'))

        # user selected the fields in form login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.get_by_name(form, 'username')
        password_field = self.get_by_name(form, 'password')

        # typing the data in fields
        username_field.send_keys(f'{user.username}')
        password_field.send_keys(f'{string_password}')

        # send form
        form.submit()

        self.assertIn(
            f'Your are logged with {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        ...

    def test_user_submit_fields_empty_raise_error_message_form_invalid(self):

        # user open browser in page login

        self.browser.get(self.live_server_url + reverse('authors:login'))

        # user selected the fields in form login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.get_by_name(form, 'username')
        password_field = self.get_by_name(form, 'password')

        # typing the data in fields
        username_field.send_keys('       ')
        password_field.send_keys('       ')

        # send form
        form.submit()

        self.assertIn(
            'invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_insert_credentials_invalid_raise_error_message(self):

        # user open browser in page login

        self.browser.get(self.live_server_url + reverse('authors:login'))

        # user selected the fields in form login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.get_by_name(form, 'username')
        password_field = self.get_by_name(form, 'password')

        # typing the data in fields
        username_field.send_keys('usertest')
        password_field.send_keys("adadad")

        # send form
        form.submit()

        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_get_in_login_create_view_raise_404(self):
        # user open browser in page login

        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        self.assertIn(

            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
