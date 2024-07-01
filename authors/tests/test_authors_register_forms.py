from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.register_form import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', (
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        )),
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    def test_form_register_in_request_get(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        field = 'username'
        self.assertIn(field, response.context['form'].fields)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
        ('email', 'E-mail is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):

        self.form_data[field] = ''

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

        ...

    @parameterized.expand(
        [
            ('username', 'Username must have at least 4 characters'),
        ]
    )
    def test_username_field_min_length_should_be_4_characters(self, field, expected):

        msg = 'joe'
        self.form_data[field] = msg
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(expected, response.context['form'].errors.get(field))

    @parameterized.expand(
        [
            ('username', 'Username must have less than 150 characters'),
        ]
    )
    def test_username_field_max_length_should_be_4_characters(self, field, expected):

        msg = 'j'*151
        self.form_data[field] = msg
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(expected, response.context['form'].errors.get(field))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):

        msg = 'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.'
        self.form_data['password'] = 'baucba'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):

        self.form_data['password'] = 'abc@12AAa'
        self.form_data['password2'] = 'baucbaa'
        msg = 'Password and password2 must be equal'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get('password2'))

    def test_whether_the_error_message_email_is_already_in_use_is_displayed_in_the_email_field(self):
        url = reverse('authors:create')
        for i in range(2):
            response = self.client.post(url, data=self.form_data, follow=True)
            """  self.form_data['email'] = 'hvxuaasxuvaxva@gmail.com' """

        msg = 'User e-mail is already in use'
        self.assertIn(msg, response.context['form'].errors.get('email'))

        ...
