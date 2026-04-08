#src/recipes/views.py
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, TemplateView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import RecipeForm
from family_tree.models import FamilyGroup

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    queryset = Recipe.objects.select_related("owner").prefetch_related(
        "allowed_families", "allowed_users"
    ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for recipe in context["recipes"]:
            recipe.can_view_details_for_user = recipe.can_view_details(
                self.request.user
            )
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_view_details"] = self.object.can_view_details(
            self.request.user
        )
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"
    success_url = reverse_lazy("recipes:recipe_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class HomeView(TemplateView):
    template_name = "recipes/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_recipes"] = Recipe.objects.select_related("owner").order_by("-created_at")[:5]
        return context
