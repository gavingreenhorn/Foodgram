from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


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