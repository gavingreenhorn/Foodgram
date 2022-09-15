from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import FoodgramUserManager


class FoodgramUser(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name='email', unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    favorites = models.ManyToManyField(to='recipes.Recipe', related_name='enjoyers', through='recipes.Favorite')
    cart = models.ManyToManyField(to='recipes.Recipe', related_name='buyers', through='recipes.ShoppingCart')
    objects = FoodgramUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'