from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser

from .managers import FoodgramUserManager


class FoodgramUser(AbstractUser):
    email = models.EmailField(max_length=254, verbose_name='email', unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    favorites = models.ManyToManyField(
        to='recipes.Recipe', related_name='enjoyers',
        through='recipes.Favorite')
    cart = models.ManyToManyField(
        to='recipes.Recipe', related_name='buyers',
        through='recipes.ShoppingCart')
    subscriptions = models.ManyToManyField(
        to='FoodgramUser', related_name='subscribers',
        through='users.Subscription')
    objects = FoodgramUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['username']


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        FoodgramUser,
        related_name='subscribed_to',
        on_delete=models.CASCADE
    )
    publisher = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "publisher"], name="UniqueSubscribe"
            ),
            models.CheckConstraint(
                check=~Q(subscriber=F('publisher')), name="SubToSelf"
            )
        ]