
from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import TestRecipeBase


class RecipeDetailViewTest(TestRecipeBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'recipe_id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_status_code_is_404_ok(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'recipe_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_load_the_correct_recipe(self):
        # needed_title
        needed_title = 'this is a detail page - it load one recipe'
        # need a recipe for this test
        self.make_recipe(title=needed_title, is_published=True)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'recipe_id': 1}))
        response_recipes_context = response.content.decode('utf-8')
        # check if one recipe exists
        self.assertIn(
            needed_title,
            response_recipes_context
        )
        ...

    def test_recipe_detail_template_wont_load_recipes_if_not_published(self):
        # need recipe not published
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe',
                    kwargs={'recipe_id': recipe.id}))
        # check if one recipe exists
        self.assertEqual(
            response.status_code,
            404
        )
