from django.contrib.auth.models import User
from django.db import models

class FamilyGroup(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FamilyMember(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="family_profile"
    )
    display_name = models.CharField(max_length=120, blank=True)
    families = models.ManyToManyField(
        FamilyGroup, related_name="members", blank=True
    )
    parents = models.ManyToManyField(
        "self", symmetrical=False, related_name="children", blank=True
    )
    spouses = models.ManyToManyField("self", symmetrical=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    generation = models.IntegerField(default=0, help_text="Generation level (0 = oldest ancestors, higher numbers = descendants)")
    display_order = models.IntegerField(default=0, help_text="Position within the generation; lower values appear first.")

    def __str__(self):
        return self.display_name or self.user.get_full_name() or self.user.username
