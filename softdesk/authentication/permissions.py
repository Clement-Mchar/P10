from rest_framework import permissions


class IsCreationOrIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == "create":
            return (
                not request.user.is_authenticated
                or request.user.is_superuser
                or request.user.is_staff
            )
        elif view.action in ["list", "retrieve"]:
            return (
                request.user.is_authenticated
                or request.user.is_superuser
                or request.user.is_staff
            )
        return True


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
