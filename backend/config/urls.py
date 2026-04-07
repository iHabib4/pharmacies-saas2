from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

print("🔥 CONFIG URLS LOADED")


# Simple root view
def home(request):
    return JsonResponse(
        {"message": "Django is running 🚀", "available_endpoints": ["/admin/", "/api/"]}
    )


urlpatterns = [
    path("", home),  # ✅ Root URL (fixes your 404)
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # This triggers api.urls
]
