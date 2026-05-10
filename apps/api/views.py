import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.pharmacies.models import Pharmacy

User = get_user_model()


@csrf_exempt
def register(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=400
        )

    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    mobile_number = data.get("mobile_number")
    password = data.get("password")
    pharmacy_name = data.get("pharmacy_name")
    role = data.get("role", "customer")

    if not mobile_number or not password:
        return JsonResponse(
            {"error": "Missing fields"},
            status=400
        )

    if User.objects.filter(
        mobile_number=mobile_number
    ).exists():

        return JsonResponse(
            {"error": "User already exists"},
            status=400
        )

    try:

        user = User.objects.create_user(
            mobile_number=mobile_number,
            password=password,
            role=role
        )

        pharmacy = None

        if role in ["pharmacy", "pharmacy_owner"]:

            pharmacy = Pharmacy.objects.create(
                name=pharmacy_name or mobile_number,
                owner=user
            )

            user.pharmacy = pharmacy
            user.save()

        return JsonResponse(
            {
                "message": "Registration successful",
                "user_id": user.id,
                "role": user.role,
                "pharmacy_id": pharmacy.id if pharmacy else None
            },
            status=201
        )

    except Exception as e:

        return JsonResponse(
            {"error": str(e)},
            status=500
        )
