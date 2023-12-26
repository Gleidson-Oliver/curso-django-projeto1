from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import TestRecipeBase


class TestRecipModels(TestRecipeBase):

    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_raises_error_if_title_has_more_that_65_chars(self):
        self.recipe.title = 'A' * 70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
        ...

    @parameterized.expand(
        [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65)
        ]
    )
    def test_fields_max_length(self, field, max_length, ):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
            ...

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        """
        testing the fail in  
        test_recipe_preparation_steps_is_html_is_false_by_default

        """
        # self.recipe.preparation_steps_is_html = True
        self.recipe.full_clean()
        self.recipe.save()
        self.assertFalse(self.recipe.preparation_steps_is_html)
        ...

    def test_recipe_is_published_is_false_by_default(self):
        """
        testing the fail in  
        test_recipe_is_published_is_false_by_default

        """
        # self.recipe.is_published = True
        self.recipe.full_clean()
        self.recipe.save()
        self.assertFalse(self.recipe.is_published)
        ...
