#src/family_tree/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import FamilyGroup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import FamilyMember, FamilyGroup

class FamilyTreeView(TemplateView):
    template_name = "family_tree/family_tree.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["families"] = FamilyGroup.objects.prefetch_related(
            "members__parents", "members__spouses"
        ).order_by("name")
        return context

class FamilyMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = FamilyMember
    fields = ['display_name', 'families', 'parents', 'spouses', 'birth_date', 'notes']
    template_name = "family_tree/member_form.html"
    success_url = reverse_lazy("family_tree:tree")

    def get_object(self):
        return self.request.user.family_profile
