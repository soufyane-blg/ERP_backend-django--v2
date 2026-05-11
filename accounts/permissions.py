from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated



class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_staff


class HasSameOrganization(BasePermission):

    def has_object_permission(self, request, view, obj):

        return (
            request.user.is_authenticated
            and obj.organization == request.user.organization
        )
    
