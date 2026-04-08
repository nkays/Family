from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "visibility", "created_at")
    search_fields = (
        "title",
        "description",
        "ingredients",
        "instructions",
        "owner__username",
    )
    list_filter = ("visibility", "created_at", "owner")
    filter_horizontal = ("allowed_users", "allowed_families")
    raw_id_fields = ("owner",)
    readonly_fields = ("created_at", "updated_at")
