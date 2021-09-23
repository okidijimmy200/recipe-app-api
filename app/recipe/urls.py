from django.urls import path, include
from rest_framework import routers, urlpatterns
from rest_framework.routers import DefaultRouter
from recipe import views

routers = DefaultRouter()

# register the view with router
routers.register('tags', views.TagViewSet)
routers.register('ingredients', views.IngredientViewSet)
routers.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(routers.urls))
]