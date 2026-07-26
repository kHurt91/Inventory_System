from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """Authenticated users may read (GET/HEAD/OPTIONS); only is_staff users may write."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_staff)
