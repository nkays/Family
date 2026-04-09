#src/family_tree/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import FamilyGroup, FamilyMember
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from collections import defaultdict

class FamilyTreeView(TemplateView):
    template_name = "family_tree/family_tree.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all unique family members across all families
        all_members = FamilyMember.objects.prefetch_related(
            "parents", "spouses", "children"
        ).distinct()
        
        # Organize members by generation using the model field
        generation_dict = defaultdict(list)
        
        for member in all_members:
            generation_dict[member.generation].append(member)
        
        # Convert to sorted list of (generation, members) tuples
        generations = [
            (gen, self._order_generation_members(members))
            for gen, members in sorted(generation_dict.items())
        ]
        
        context["all_members"] = all_members
        context["generations"] = generations
        context["families"] = FamilyGroup.objects.prefetch_related(
            "members__parents", "members__spouses"
        ).order_by("name")
        
        return context

    def _order_generation_members(self, members):
        ordered_members = sorted(
            members,
            key=lambda member: (member.display_order, member.display_name.lower() if member.display_name else member.user.username.lower())
        )

        member_map = {member.id: member for member in ordered_members}
        result = []
        seen = set()

        for member in ordered_members:
            if member.id in seen:
                continue
            result.append(member)
            seen.add(member.id)

            spouse_partners = [
                spouse for spouse in member.spouses.all()
                if spouse.id in member_map and spouse.id not in seen
            ]
            spouse_partners.sort(
                key=lambda spouse: (spouse.display_order, spouse.display_name.lower() if spouse.display_name else spouse.user.username.lower())
            )

            for spouse in spouse_partners:
                result.append(spouse)
                seen.add(spouse.id)

        return result

class FamilyMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = FamilyMember
    fields = ['display_name', 'families', 'parents', 'spouses', 'birth_date', 'notes']
    template_name = "family_tree/member_form.html"
    success_url = reverse_lazy("family_tree:tree")

    def get_object(self):
        return self.request.user.family_profile
