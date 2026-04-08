from django.contrib.auth.models import User
from django.db import models

class Recipe(models.Model):
    VISIBILITY_PUBLIC = "PUBLIC"
    VISIBILITY_FAMILY = "FAMILY"
    VISIBILITY_SPECIFIC = "SPECIFIC"

    VISIBILITY_CHOICES = [
        (VISIBILITY_PUBLIC, "Public"),
        (VISIBILITY_FAMILY, "Family only"),
        (VISIBILITY_SPECIFIC, "Specific people"),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="recipe_photos/", blank=True, null=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default=VISIBILITY_FAMILY
    )
    allowed_users = models.ManyToManyField(
        User, related_name="shared_recipes", blank=True
    )
    allowed_families = models.ManyToManyField(
        "family_tree.FamilyGroup", related_name="shared_recipes", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def can_view_details(self, user):
        if self.visibility == self.VISIBILITY_PUBLIC:
            return True
        if not user or not user.is_authenticated:
            return False
        if user == self.owner:
            return True
        if self.allowed_users.filter(pk=user.pk).exists():
            return True
        if self.visibility == self.VISIBILITY_FAMILY:
            user_profile = getattr(user, "family_profile", None)
            owner_profile = getattr(self.owner, "family_profile", None)
            if self.allowed_families.exists():
                return (
                    user_profile
                    and user_profile.families.filter(
                        pk__in=self.allowed_families.values_list("pk", flat=True)
                    ).exists()
                )
            if owner_profile and user_profile:
                return user_profile.families.filter(
                    pk__in=owner_profile.families.values_list("pk", flat=True)
                ).exists()
        return False
