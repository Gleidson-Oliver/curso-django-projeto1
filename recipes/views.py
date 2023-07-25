# from django.http import HttpResponse
from django.shortcuts import render

from utils.recipe.factory import make_recipe


# Create your views here.
def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)]
    })
    make_recipe()


def recipes(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'detail_page': True,
    })
