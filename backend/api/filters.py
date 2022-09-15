from rest_framework.filters import SearchFilter
from urllib.parse import unquote
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class Klyukva(SearchFilter):
    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')
        params = params.replace(',', ' ')
        params = unquote(params)
        return params.split()


class IngredientFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilterSet(filters.FilterSet):
    author = filters.CharFilter(field_name="id", lookup_expr='exact')
    tags = filters.CharFilter(field_name="tags__slug", lookup_expr='exact')
    

    class Meta:
        model = Recipe
        fields = ('author',)