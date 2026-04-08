from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'photo', 'ingredients', 'instructions', 'visibility', 'allowed_users', 'allowed_families']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 5}),
            'instructions': forms.Textarea(attrs={'rows': 10}),
            'allowed_users': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'allowed_families': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }