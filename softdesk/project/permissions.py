from rest_framework import permissions

class IsAuthorOrStaffOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user 
            

'''class IsNotContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user not in obj.contributors.all()'''