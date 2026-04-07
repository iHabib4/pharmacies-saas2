from django.http import JsonResponse
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


# Optional: API root endpoint (fixes /api/)
def api_root(request):
    return JsonResponse(
        {
            "message": "API is working 🚀",
            "endpoints": [
                "/api/auth/login/",
                "/api/auth/refresh/",
                "/api/users/",
                "/api/pharmacies/",
                "/api/products/",
                "/api/orders/",
                "/api/payments/",
                "/api/riders/",
                "/api/tracking/",
                "/api/deliveries/",
            ],
        }
    )


urlpatterns = [
    # ✅ Root API (IMPORTANT)
    path("", api_root),
    # ✅ JWT Authentication
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ✅ Project apps
    path("users/", include("apps.users.urls")),
    path("pharmacies/", include("apps.pharmacies.urls")),
    path("products/", include("apps.products.urls")),
    path("orders/", include(("apps.orders.urls", "orders"), namespace="orders")),
    path("payments/", include("apps.payments.urls")),
    path("riders/", include("apps.riders.urls")),
    path("tracking/", include("apps.tracking.urls")),
    path("deliveries/", include("apps.deliveries.urls")),
]
