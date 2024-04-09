from rest_framework import permissions

class IsCreationOrIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return not request.user.is_authenticated or request.user.is_superuser or request.user.is_staff
        elif request.method in permissions.SAFE_METHODS:
            return True
        return True


'''class IsNotContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user not in obj.contributors.all()'''