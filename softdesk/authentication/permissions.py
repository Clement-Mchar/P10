from rest_framework import permissions


class IsCreationOrIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == "create":
            return (
                not request.user.is_authenticated
                or request.user.is_superuser
                or request.user.is_staff
            )
        elif view.action == "list":
            return (
                request.user.is_authenticated
                or request.user.is_superuser
                or request.user.is_staff
            )
        return True
