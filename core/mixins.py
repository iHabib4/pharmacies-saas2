class PharmacyQuerysetMixin:
    """
    Automatically filters queryset by request.pharmacy
    (SaaS multi-tenant isolation layer)
    """

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        pharmacy = getattr(self.request, "pharmacy", None)

        # Admin sees everything
        if user.is_authenticated and getattr(user, "role", None) == "admin":
            return queryset

        # Pharmacy users only see their own data
        if pharmacy:
            return queryset.filter(pharmacy=pharmacy)

        # No access if no pharmacy
        return queryset.none()
