from django.urls import path
from .views import RecipeCreateView, RecipeDetailView, RecipeListView

app_name = "recipes"

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("create/", RecipeCreateView.as_view(), name="recipe_create"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
]