from rest_framework.permissions import BasePermission


# =========================
# ROLE PERMISSIONS
# =========================

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or
            getattr(request.user, "role", "") == "admin"
        )


class IsPharmacy(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, "role", "") in ["pharmacy", "pharmacy_owner"]
        )


class IsRider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, "role", "") == "rider"
        )


class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, "role", "") == "supplier"
        )


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, "role", "") == "customer"
        )


# =========================
# ACTION PERMISSIONS
# =========================

class CanManageUsers(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or
            getattr(request.user, "role", "") == "admin"
        )


class CanManageProducts(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, "role", "") in ["admin", "pharmacy", "supplier"]
        )


class CanManageOrders(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, "role", "") in ["admin", "pharmacy", "rider"]
        )


class CanViewAnalytics(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            getattr(request.user, "role", "") == "admin"
        )
