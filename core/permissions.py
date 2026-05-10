from rest_framework.permissions import BasePermission


# =========================
# ADMIN
# =========================
class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and (
                user.is_superuser or
                user.is_staff or
                getattr(user, "role", "") == "admin"
            )
        )


# =========================
# PHARMACY
# =========================
class IsPharmacy(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and
            getattr(user, "role", "") in [
                "pharmacy",
                "pharmacy_owner"
            ]
        )


# =========================
# SUPPLIER
# =========================
class IsSupplier(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and
            getattr(user, "role", "") == "supplier"
        )


# =========================
# RIDER
# =========================
class IsRider(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and
            getattr(user, "role", "") == "rider"
        )


# =========================
# CUSTOMER
# =========================
class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and
            getattr(user, "role", "") == "customer"
        )


# =========================
# ACTION-LEVEL RBAC
# =========================
class CanManageUsers(BasePermission):

    def has_permission(self, request, view):
        return IsAdmin().has_permission(request, view)


class CanManageProducts(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and (
                user.is_superuser or
                user.role in [
                    "admin",
                    "pharmacy",
                    "pharmacy_owner",
                    "supplier"
                ]
            )
        )


class CanManageOrders(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and (
                user.is_superuser or
                user.role in [
                    "admin",
                    "pharmacy",
                    "pharmacy_owner",
                    "rider"
                ]
            )
        )


class CanViewAnalytics(BasePermission):

    def has_permission(self, request, view):
        return IsAdmin().has_permission(request, view)
