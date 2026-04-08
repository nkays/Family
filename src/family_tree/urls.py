from django.urls import path
from .views import FamilyMemberUpdateView, FamilyTreeView

app_name = "family_tree"

urlpatterns = [
    path("", FamilyTreeView.as_view(), name="tree"),
    path("profile/edit/", FamilyMemberUpdateView.as_view(), name="member_update"),
]