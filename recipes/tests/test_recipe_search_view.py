
from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import TestRecipeBase


class RecipeSearchViewTest(TestRecipeBase):

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search',)+'?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_empty_return_page_home(self):
        response = self.client.get(reverse('recipes:search',) + '?q= ')
        print(response)
        url_home = '/'
        self.assertEqual(response.url, url_home)

    def test_recipe_search_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search')+'?q="testes"')

        self.assertIn('&quot;testes&quot', response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'this is recipe one'
        title2 = 'this is recipe two'
        url_search = reverse('recipes:search')

        recipe1 = self.make_recipe(title=title1, authors_data={
                                   'username': 'one'}, slug='one',)
        recipe2 = self.make_recipe(title=title2, authors_data={
                                   'username': 'two'}, slug='two')

        response1 = self.client.get(f'{url_search}?q={title1}')
        response2 = self.client.get(reverse('recipes:search') + f'?q={title2}')
        response_both = self.client.get(reverse('recipes:search') + '?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])

        self.assertNotIn(recipe1, response2.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
