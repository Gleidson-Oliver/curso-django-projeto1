
from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_whitout_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep()
        self.assertIn('No recipes found here 🥲', body.text)

    def test_recipe_search_input_can_find_correct_recipes(self):

        # creating recipes
        recipes = self.make_recipe_in_batch()

        # required title
        needed = 'this is what I need'

        # renaming recipe title  one
        recipes[0].title = needed
        recipes[0].save()

        # accessing the website's home page
        self.browser.get(self.live_server_url)

        # find the placeholder entry "search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH, '//input[@placeholder = "Search for a recipe"]')

        # typing the title and pressing enter
        search_input.send_keys(needed)
        search_input.send_keys(Keys.ENTER)
        self.sleep()

        # find the class recipe-title-container
        recipe_title_html_class = "recipe-title-container"

        search_title = self.browser.find_element(
            By.CLASS_NAME, recipe_title_html_class)

        # checking if the required title  is in class html element "recipe-title-container"
        self.assertIn(needed, search_title.text)
        self.browser.quit()

    @patch('recipes.views.PER_PAGE', new=5)
    def test_recipe_home_page_pagination(self):
        # creating recipes
        self.make_recipe_in_batch()

        # accessing the website's home page
        self.browser.get(self.live_server_url)

        # find the placeholder entry "search for a recipe"
        aria_label_nav = self.browser.find_element(
            By.XPATH, '//nav[@aria-label = "Main Pagination"]')

        aria_label_nav.click()

        # click in page 2
        aria_label_a = self.browser.find_element(
            By.XPATH, '/html/body/main/nav/div/a[2]')

        aria_label_a.click()

        # checking if the number of recipes  is equal to 5 on page 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 5
        )
