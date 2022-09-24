from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet

from .views import (IngredientViewSet, RecipeViewSet,
                    TagViewSet, FoodgramUsersViewset)

app_name = 'api'

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags'),
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('users/',
         UserViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='user-list'),
    path('users/<int:id>/',
         UserViewSet.as_view({'get': 'retrieve'}),
         name='user-detail'),
    path('users/me/',
         UserViewSet.as_view({'get': 'me'}),
         name='profile'),
    path('users/set_password/',
         UserViewSet.as_view({'post': 'set_password'}),
         name='set-password'),
    path('users/<int:id>/subscribe/',
         FoodgramUsersViewset.as_view(
            {'post': 'subscribe', 'delete': 'subscribe'}),
         name='subscribe'),
    path('users/subscriptions/',
         FoodgramUsersViewset.as_view({'get': 'subscriptions'}),
         name='subscriptions'),
    path('auth/', include('djoser.urls.authtoken')),
]
