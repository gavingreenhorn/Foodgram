from http.client import HTTPResponse
import os
import re
import csv
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework import viewsets, mixins, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError

from djoser.views import UserViewSet
from recipes.models import Favorite, Recipe, Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer, RecipeShortSerializer, RecipeSerializer, FoodgramUserSerializer, SubscriptionSerializer
from .filters import IngredientFilterSet, RecipeFilterSet

User = get_user_model()

ERR_NAME = re.compile(r'(?<=: ).*$')


class FoodgramUsersViewset(UserViewSet):

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('subscribe', 'subscriptions'):
            return SubscriptionSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'subscribe':
            context.setdefault('object', self.get_object())
        return context

    def get_queryset(self):
        if self.action == 'subscriptions':
            return self.request.user.subscriptions.all()
        return super().get_queryset()

    def create_sub(self, *args, **kwargs):
        return self.request.user.subscriptions.add(self.get_object())

    def remove_sub(self, *args, **kwargs):
        self.request.user.subscriptions.remove(self.get_object())

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        if request.method == "POST":
            self.perform_create = self.create_sub
            try:
                return self.create(request, *args, **kwargs)
            except IntegrityError as ex:
                detail = str(ex)
                if str(ex).startswith('UNIQUE'):
                    detail = 'Already subscribed'
                elif str(ex).startswith('CHECK'):
                    detail = ERR_NAME.search(str(ex)).group(0)
                raise serializers.ValidationError(
                    detail=detail,
                    code=HTTPStatus.BAD_REQUEST
                )
        self.perform_destroy = self.remove_sub
        return self.destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)


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

    def get_queryset(self):
        if self.action == 'download_shopping_cart':
            return self.request.user.cart.all()
        return super().get_queryset()

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

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients = ((component.ingredient.name, component.amount)
                        for recipe in self.get_queryset()
                        for component in recipe.components.all())
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="shopping_list.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(('ingredient', 'amount'))
        for ingredient in ingredients:
            writer.writerow(ingredient)
        return response