from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets, mixins, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Favorite, Recipe, Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer, RecipeShortSerializer, RecipeSerializer
from .filters import IngredientFilterSet, RecipeFilterSet

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilterSet


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]
    filterset_class = RecipeFilterSet

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('favorite', 'shopping_cart'):
            return RecipeShortSerializer
        return RecipeSerializer
        
    def get_serializer(self, *args, **kwargs):
        if self.action in ('favorite', 'shopping_cart'):
            kwargs.setdefault('instance', self.get_object())
        return super().get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def make_favorite(self, *args, **kwargs):
        return self.request.user.favorites.add(self.get_object())

    def remove_favorite(self, *args, **kwargs):
        self.request.user.favorites.remove(self.get_object())

    def add_to_cart(self, *args, **kwargs):
        return self.request.user.cart.add(self.get_object())

    def remove_from_cart(self, *args, **kwargs):
        self.request.user.cart.remove(self.get_object())

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        if request.method == "POST":
            self.perform_create = self.make_favorite
            return self.create(request, *args, **kwargs)
        self.perform_destroy = self.remove_favorite
        return self.destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, *args, **kwargs):
        if request.method == "POST":
            self.perform_create = self.add_to_cart
            return self.create(request, *args, **kwargs)
        self.perform_destroy = self.remove_from_cart
        return self.destroy(request, *args, **kwargs)
