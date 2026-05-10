from django.http import JsonResponse
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        if request.user.role != "admin":
            return JsonResponse({"error": "Admin only"}, status=403)

        return view_func(request, *args, **kwargs)

    return wrapper
