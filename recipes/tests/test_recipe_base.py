
from django.test import TestCase

from recipes.models import Category, Recipe, User


class TestRecipeBase(TestCase):

    def setUp(self) -> None:

        return super().setUp()

    def make_category(self, name):
        return Category.objects.create(name='category_test')

    def make_authors(
        self,
        first_name='davi_test',
        last_name='santos_test',
        username='user',
        email='davi@gmail.com',
        password='12345'
    ):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )

    def make_recipe(
            self,
            category_data=None,
            authors_data=None,
            title='Recipe title test',
            description='test description',
            slug='test-slug',
            preparation_time='10',
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='servings_unit test',
            preparation_steps='recipe preparation steps test',
            preparation_steps_is_html=False,
            is_published=False
    ):

        if category_data is None:
            category_data = {}

        if authors_data is None:
            authors_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data, name='default'),
            authors=self.make_authors(**authors_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published
        )
