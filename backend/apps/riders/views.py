from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Rider
from .serializers import RiderSerializer

User = get_user_model()


# ------------------------------
# 1️⃣ Rider ViewSet
# ------------------------------
class RiderViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Rider objects.
    """

    queryset = Rider.objects.all()
    serializer_class = RiderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Admin → see all riders
        Normal user → see only their rider profile
        """
        user = self.request.user
        if user.is_staff:
            return Rider.objects.all()
        return Rider.objects.filter(user=user)


# ------------------------------
# 2️⃣ Register Rider (PUBLIC)
# ------------------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def register_rider(request):
    """
    Register a new rider (pending approval by admin).
    """
    data = request.data

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    phone = data.get("phone")
    vehicle_type = data.get("vehicle_type")

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Create the user
    user = User.objects.create_user(username=username, password=password, email=email)

    # Create the rider record
    rider = Rider.objects.create(
        user=user,
        phone=phone,
        vehicle_type=vehicle_type,
        is_approved=False,  # Must be approved by admin
    )

    return Response(
        {
            "message": "Rider registered successfully. Await admin approval.",
            "rider_id": rider.id,
        },
        status=status.HTTP_201_CREATED,
    )


# ------------------------------
# 3️⃣ Update Location (PROTECTED)
# ------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_location(request):
    """
    Update rider's current location.
    """
    try:
        rider = Rider.objects.get(user=request.user)
    except Rider.DoesNotExist:
        return Response({"error": "Rider not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        latitude = float(request.data.get("latitude"))
        longitude = float(request.data.get("longitude"))
    except (TypeError, ValueError):
        return Response(
            {"error": "Invalid latitude or longitude"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    rider.latitude = latitude
    rider.longitude = longitude
    rider.save()

    return Response(
        {
            "message": "Location updated",
            "latitude": rider.latitude,
            "longitude": rider.longitude,
        },
        status=status.HTTP_200_OK,
    )
