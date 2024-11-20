from rest_framework import permissions

class IsAuthenticatedAndAdmin(permissions.BasePermission):
    """
    Allows access only to authenticated users who are in the ADMIN group.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # Check if the user is in the ADMIN group
        return request.user.role in ['admin']