# core/middleware.py

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # import INSIDE function (important)
        from apps.tracking.models import AuditLog

        # example safe logging (adjust fields to your model)
        if request.user.is_authenticated:
            AuditLog.objects.create(
                user=request.user,
                action=request.method,
                path=request.path,
            )

        return response
