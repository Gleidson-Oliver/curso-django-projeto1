from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import TestRecipeBase


class TestRecipModels(TestRecipeBase):

    def setUp(self) -> None:
        self.category = self.make_category(name='category testing')
        return super().setUp()

    def test_recipe_category_string_representation_is_name_field(self):

        self.assertEqual(str(self.category), self.category.name)
        ...

    def test_recipe_category_model_name_max_legth_is_65_chars(self):
        self.category.name = 'A'*66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
