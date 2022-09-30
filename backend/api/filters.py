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
    is_favorited = filters.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter')

    def is_favorited_filter(self, queryset, name, value):
        if value == 1:
            queryset = queryset.filter(favorite__enjoyer=self.request.user)
        elif value == 0:
            queryset = queryset.exclude(favorite__enjoyer=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value == 1:
            queryset = queryset.filter(shoppingcart__buyer=self.request.user)
        elif value == 0:
            queryset = queryset.exclude(shoppingcart__buyer=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author',)