from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(csrf_exempt, name="dispatch")
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        items = request.data.get("items", [])
        address = request.data.get("delivery_address", "")

        if not items:
            return Response(
                {"error": "No items provided"},
                status=400
            )

        return Response(
            {
                "message": "Order received",
                "items": items,
                "delivery_address": address
            },
            status=201
        )
