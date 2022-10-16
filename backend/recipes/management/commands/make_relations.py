import os
import random

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.conf import settings
from recipes.models import Tag, Ingredient, Recipe, Component

from ._utils import get_image

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            for i in range(1, 4):
                img_path = os.path.join(
                    settings.BASE_DIR,
                    f'static/data/dummy_images/{i}.jpg')
                recipe = Recipe.objects.create(
                    author_id=i, name=f"test_recipe_{i}",
                    cooking_time="40", image=get_image(img_path))
                tags = Tag.objects.filter(pk__in=range(i, i + 2))
                r = random.randint(4, Ingredient.objects.all().count())
                ingredients = Ingredient.objects.filter(pk__in=range(r - 3, r))
                recipe.tags.add(*tags)
                for ingredient in ingredients:
                    Component.objects.create(
                        recipe=recipe, ingredient=ingredient,
                        amount=random.randint(10, 400))
        except Exception as ex:
            raise CommandError(ex)
        else:
            self.stdout.write(self.style.SUCCESS(
                'Successfully created recipe objects'))
