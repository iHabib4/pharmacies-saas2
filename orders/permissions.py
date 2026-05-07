from rest_framework.permissions import BasePermission


def has_role(request, roles):
    return (
        request.user
        and request.user.is_authenticated
        and getattr(request.user, "role", None) in roles
    )


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return has_role(request, ["customer"])


class IsPharmacyOwner(BasePermission):
    def has_permission(self, request, view):
        return has_role(request, ["pharmacy", "pharmacy owner"])


class IsRider(BasePermission):
    def has_permission(self, request, view):
        return has_role(request, ["rider"])


class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        return has_role(request, ["supplier"])


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return has_role(request, ["admin"])
