from rest_framework import permissions
from .models import Project
from authentication.models import Contributor

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class IsContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        return Contributor.objects.filter(user_id=request.user.id, project_id=view.kwargs["project_pk"]).exists()
