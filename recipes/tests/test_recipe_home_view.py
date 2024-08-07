
from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import TestRecipeBase


class RecipeHomeViewTest(TestRecipeBase):

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
        ...

    def test_recipe_home_view_returns_status_code_is_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_show_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found here 🥲',
            response.content.decode('utf-8')
        )

    @patch('recipes.views.PER_PAGE', new=10)
    def test_recipe_home_pagination_load_correct_expected_range(self):

        self.make_recipe_in_batch(qtd=20)

        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 2)

    def test_recipe_home_template_load_recipes(self):
        # need a recipe for this test
        self.make_recipe(is_published=True)

        response = self.client.get(reverse('recipes:home'))
        response_recipes_context = response.content.decode('utf-8')

        # check if one recipe exists
        self.assertIn(
            'Recipe title test',
            response_recipes_context
        )
        ...

    def test_recipe_home_template_wont_load_recipes_if_not_published(self):
        # need recipe not published
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        # check if one recipe exists
        self.assertIn(
            'No recipes found here 🥲',
            content
        )
        # self.assertEqual()
        ...

    @patch('recipes.views.PER_PAGE', new=3)
    def test_invalid_page_query_uses_page_one(self):

        self.make_recipe_in_batch(qtd=8)

        response = self.client.get(reverse('recipes:home') + '?page=1A21')
        ...
        self.assertEqual(response.context['recipes'].number, 1)
