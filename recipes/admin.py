from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Category, Recipe

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    #
    ...

# outra maneira de registrar a model no admin do django


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
