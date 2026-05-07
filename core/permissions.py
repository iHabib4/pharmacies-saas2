from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Only users with role = admin can access.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == "admin"
        )
