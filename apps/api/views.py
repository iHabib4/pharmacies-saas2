import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.pharmacies.models import Pharmacy  # adjust path if needed

# Use your custom user model
User = get_user_model()


@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email")
    password = data.get("password")
    pharmacy_name = data.get("pharmacy_name")

    if not email or not password or not pharmacy_name:
        return JsonResponse({"error": "Missing fields"}, status=400)

    # Check if user already exists
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already registered"}, status=400)

    try:
        # Create user
        user = User.objects.create_user(username=email, email=email, password=password)

        # Create pharmacy linked to user
        pharmacy = Pharmacy.objects.create(name=pharmacy_name, owner=user)

        # Return success JSON
        return JsonResponse(
            {
                "message": "Registration successful",
                "user_id": user.id,
                "pharmacy_id": pharmacy.id,
            },
            status=201,
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
