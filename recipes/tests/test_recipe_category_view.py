
from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import TestRecipeBase


class RecipeCategoryViewTest(TestRecipeBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)
        print("esse é o print", view)

    def test_recipe_category_template_load_recipes(self):
        # needed_title
        needed_title = 'this is a title test'
        # need a recipe for this test
        self.make_recipe(title=needed_title, is_published=True)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        response_recipes_context = response.content.decode('utf-8')
        # check if one recipe exists
        self.assertIn(
            needed_title,
            response_recipes_context
        )
        ...

    def test_recipe_category_view_returns_status_code_is_404_ok(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_wont_load_recipes_if_not_published(self):
        # need recipe not published
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.id}))
        # check if one recipe exists
        self.assertEqual(
            response.status_code,
            404
        )
