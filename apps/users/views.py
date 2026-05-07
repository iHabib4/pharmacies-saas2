from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer, UserRegisterSerializer

User = get_user_model()

class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "ok": True,
            "user_id": user.id,
            "mobile_number": user.mobile_number,
            "role": user.role,
            "profile_picture": (
                request.build_absolute_uri(user.profile_picture.url)
                if user.profile_picture else None
            ),
        })

# =========================
# REGISTER
# =========================
class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("❌ REGISTER ERROR:", serializer.errors)
            return Response(serializer.errors, status=400)

        self.perform_create(serializer)
        return Response(serializer.data, status=201)


# =========================
# LOGIN
# =========================
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        input_value = (
            request.data.get("input")
            or request.data.get("phone")
            or request.data.get("email")
        )
        password = request.data.get("password")

        if not input_value or not password:
            return Response(
                {"error": "Input and password required"},
                status=400
            )

        user = None

        # try phone
        try:
            user = User.objects.get(mobile_number=input_value)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=input_value)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials"},
                    status=400
                )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"},
                status=400
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "name": user.username,
                "role": user.role,
                "phone": user.mobile_number,
                "email": user.email,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
            }
        })


# =========================
# LOGOUT
# =========================
class LogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "Refresh token required"},
                    status=400
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=200
            )

        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=400
            )


# =========================
# USER DETAIL (/me)
# =========================
class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "ok": True,
            "user_id": request.user.id,
            "mobile_number": request.user.mobile_number,
            "role": request.user.role,
        })

# =========================
# PASSWORD RESET REQUEST
# =========================
class PasswordResetRequestAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email required"}, status=400)

        return Response({"message": "If email exists, reset link sent"})


# =========================
# PASSWORD RESET CONFIRM
# =========================
class PasswordResetConfirmAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        password = request.data.get("password")

        if not password:
            return Response({"error": "Password required"}, status=400)

        return Response({"message": "Password reset successful"})


# =========================
# TOGGLE USER ACTIVE STATUS
# =========================
class ToggleUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.is_active = not user.is_active
            user.save()

            return Response({
                "message": "User status updated",
                "is_active": user.is_active
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({
                "error": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
