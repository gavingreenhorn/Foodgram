from dataclasses import fields
from email.policy import default
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, Component, Tag, Favorite

User = get_user_model()


class FoodgramUserSerializer(UserSerializer):
    """Return subscription field in response"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return 'TBD'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagField(serializers.PrimaryKeyRelatedField):
    class Meta:
        model = Tag
        fields = '__all__'
    
    def to_representation(self, value):
        return TagSerializer(value).data


class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        fields = '__all__'
        read_only_fields = ('recipe',)


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagField(many=True, queryset=Tag.objects.all())
    ingredients = ComponentSerializer(many=True, source="components")

    def get_is_favorited(self, obj):
        return "TBD"

    def get_is_in_shopping_cart(self, obj):
        return "TBD"

    class Meta:
        model = Recipe
        exclude = ['image']

    def create(self, validated_data):
        components = validated_data.pop("components")
        instance = super().create(validated_data)
        for component in components:
            instance.components.create(ingredient=component['ingredient'], amount=component['amount'])
        return instance


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')