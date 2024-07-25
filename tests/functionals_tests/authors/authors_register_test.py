import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def get_form(self):
        return self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form')

    def fill_form_dummy_data(self, form):

        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' '*20)

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        self.get_by_name(form, 'email').send_keys('dummys@gmail.com')

        callback(form)
        return form

    def test_authors_register(self):
        self.browser.get(self.live_server_url + '/authors/register/')

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name = self.get_by_placeholder(form, 'Ex.: John')
            first_name.send_keys(' ')
            first_name.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name.send_keys(' ')
            last_name.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username = self.get_by_placeholder(form, 'Your username')
            username.send_keys(' ')
            username.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_password_do_not_match(self):
        def callback(form):
            password = self.get_by_placeholder(form, 'Type your password')
            password2 = self.get_by_placeholder(form, 'Repeat your password')
            password.send_keys('@Aa123456')
            password2.send_keys('@Aa1234567')
            password.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Password and password2 must be equal', form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_is_successfuly(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.get_form()

        self.get_by_name(form, 'first_name').send_keys('First name')
        self.get_by_name(form, 'last_name').send_keys('Last name')
        self.get_by_name(form, 'username').send_keys('username')
        self.get_by_name(form, 'email').send_keys('dummy@gmail.com')
        self.get_by_name(form, 'password').send_keys('@Aa1234567')
        self.get_by_name(form, 'password2').send_keys('@Aa1234567')

        form.submit()

        self.assertIn('usuario registrado com sucesso',
                      self.browser.find_element(By.TAG_NAME, 'body').text
                      )
