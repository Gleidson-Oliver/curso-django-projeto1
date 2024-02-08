# from django.http import HttpResponse
import os

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import (HttpResponse, get_list_or_404, get_object_or_404,
                              render)

from utils.pagination import make_pagination

from .models import Recipe

PER_PAGE = os.environ.get('PER_PAGE', 4)


def home(request):
    recipe = Recipe.objects.filter(
        is_published=True).order_by("-id")

    obj_page, pagination_range = make_pagination(
        request, recipe, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': obj_page,
        'pagination_range': pagination_range,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(
        request, recipes, per_page=PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe,
                               pk=recipe_id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'detail_page': True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipe = Recipe.objects.filter(
        Q(title__icontains=search_term) | Q(description__icontains=search_term) | Q(category__name__icontains=search_term)).order_by('-id')

    if not recipe:
        messages.error(
            request, f"""
            oi, vi que vc pesquisou por ( {search_term} ),
            infelizmente não existem resultados para esta pesquisa""")
    else:
        messages.success(
            request, f'oi, vi que vc pesquisou por ( {search_term} ), segue abaixo os resultados')

    obj_page, pagination_range = make_pagination(
        request, recipe, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'for search "{search_term}"',
        'search_term': search_term,
        'recipes': obj_page,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
    })
