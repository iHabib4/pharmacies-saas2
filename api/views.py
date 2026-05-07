from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    return JsonResponse({"message": "API is working 🚀"})


@api_view(['GET'])
def me(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
    })
