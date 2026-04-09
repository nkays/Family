from django.contrib import admin
from .models import FamilyGroup, FamilyMember

@admin.register(FamilyGroup)
class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "generation", "display_order")
    search_fields = ("display_name", "user__username", "user__email")
    filter_horizontal = ("families", "parents", "spouses")
    raw_id_fields = ("user",)
    list_editable = ("generation", "display_order")
    list_editable = ("generation",)
