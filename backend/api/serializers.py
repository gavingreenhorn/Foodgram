from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from recipes.models import Recipe, Ingredient, Component, Tag
from .fields import Base64ImageField

User = get_user_model()


class FoodgramUserSerializer(UserSerializer):
    """Return subscription field in response"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_subscribed',)
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return (self.context['request'].user.is_authenticated and
                obj in self.context['request'].user.subscriptions.all())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['password']
        return data


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

    def to_representation(self, instance):
        return TagSerializer(instance).data


class ComponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Component
        fields = '__all__'
        read_only_fields = ('recipe',)

    def to_representation(self, instance):
        return {
            'id': instance.ingredient.id,
            'name': instance.ingredient.name,
            'measurement_unit': instance.ingredient.measurement_unit,
            'amount': instance.amount}

    def to_internal_value(self, data):
        data['ingredient'] = data.pop('id')
        return super().to_internal_value(data)

    def validate_amount(self, value):
        try:
            return int(value)
        except Exception:
            raise serializers.ValidationError("Non-digit value")


class RecipeSerializer(serializers.ModelSerializer):
    author = FoodgramUserSerializer(read_only=True)
    tags = TagField(many=True, queryset=Tag.objects.all())
    ingredients = ComponentSerializer(many=True, source="components")
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj in user.favorites.all()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj in user.cart.all()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('is_favorited', 'is_in_shopping_cart')

    def create(self, validated_data):
        components = validated_data.pop("components")
        validated_data['author'] = self.context['request'].user
        instance = super().create(validated_data)
        for component in components:
            instance.components.create(
                ingredient=component['ingredient'],
                amount=component['amount'])
        return instance

    def update(self, instance, validated_data):
        components = validated_data.pop("components")
        for field in validated_data:
            if field and getattr(instance, field):
                instance.field = validated_data[field]
        for component in components:
            if component['ingredient'] in instance.ingredients.all():
                continue
            instance.components.create(
                ingredient=component['ingredient'],
                amount=component['amount'])
        instance.save()
        return instance


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(FoodgramUserSerializer):
    recipes = RecipeShortSerializer(many=True, read_only=True)

    class Meta(FoodgramUserSerializer.Meta):
        fields = FoodgramUserSerializer.Meta.fields + ('recipes',)
        read_only_fields = (
            'username', 'first_name', 'last_name', 'email', 'password')

    def to_representation(self, instance):
        request = self.context['request']
        if request.method in ('POST', 'DELETE'):
            instance = self.context['object']
        data = super().to_representation(instance)
        if request.method == 'GET' and (cap := request.query_params.get(
                'recipes_limit', None)):
            data['recipes'] = data['recipes'][:int(cap)]
        return data
