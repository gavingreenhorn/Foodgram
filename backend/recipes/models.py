from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(
        max_length=25,
        blank=False)
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE)
    text = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(
        to='Ingredient',
        through='Component')
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes')
    image = models.ImageField(upload_to='recipes/images/')

    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Favorite(models.Model):
    enjoyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("enjoyer", "recipe"),
                                    name='UniqueFavorite')]


class ShoppingCart(models.Model):
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("buyer", "recipe"),
                                    name='UniqueCartItem')]


class Component(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='components',
        on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipes',
        on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("recipe", "ingredient"),
                                    name='UniqueComponent')]
