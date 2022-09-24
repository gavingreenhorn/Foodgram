# from django.core.management.base import BaseCommand, CommandError
# from django.contrib.auth import get_user_model

# from recipes.models import Tag, Ingredient, Recipe

# User = get_user_model()


# class Command(BaseCommand):

#     def handle(self, *args, **options):
#         for i in range(1, 4):
#             recipe = Recipe.objects.create(
#                 author_id=i, name=f"test_recipe_{i}", cooking_time="40")
#             tag = Tag.objects.get(pk=i)
#             tag_2 = Tag.objects.get(pk=i+1)
#             recipe.tags.add(tag)
#             recipe.tags.add(tag_2)
