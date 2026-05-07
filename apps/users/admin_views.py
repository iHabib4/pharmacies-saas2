from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import traceback

User = get_user_model()


# =========================
# ADMIN DASHBOARD
# =========================
class AdminDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            print("🔥 USER:", request.user)
            print("🔥 AUTH:", request.auth)

            users = User.objects.all()

            data = {
                "total_users": users.count(),
                "customers": users.filter(role="customer").count(),
                "riders": users.filter(role="rider").count(),
                "pharmacies": users.filter(role="pharmacy").count(),
                "suppliers": users.filter(role="supplier").count(),
            }

            print("🔥 DASHBOARD DATA:", data)

            return Response(data)

        except Exception:
            print("🔥🔥 ADMIN DASHBOARD CRASH:")
            print(traceback.format_exc())

            return Response(
                {"error": "Internal server error"},
                status=500
            )


# =========================
# ADMIN USERS MANAGEMENT
# =========================
class AdminUsersAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    # GET ALL USERS
    def get(self, request):
        try:
            users = User.objects.all()

            data = list(users.values(
                "id",
                "mobile_number",
                "email",
                "role",
                "is_active",
            ))

            return Response(data)

        except Exception:
            print("🔥 USERS GET ERROR:")
            print(traceback.format_exc())

            return Response(
                {"error": "Internal server error"},
                status=500
            )

    # CREATE USER
    def post(self, request):
        try:
            data = request.data

            user = User.objects.create_user(
                email=data.get("email"),
                mobile_number=data.get("mobile_number"),
                password=data.get("password"),
                role=data.get("role", "customer"),
            )

            return Response({
                "message": "User created",
                "id": user.id
            })

        except Exception:
            print("🔥 USERS CREATE ERROR:")
            print(traceback.format_exc())

            return Response(
                {"error": "User creation failed"},
                status=400
            )

    # DELETE USER
    def delete(self, request):
        try:
            user_id = request.query_params.get("id")

            if not user_id:
                return Response(
                    {"error": "User ID required"},
                    status=400
                )

            user = User.objects.get(id=user_id)

            if user.is_superuser:
                return Response(
                    {"error": "Cannot delete admin"},
                    status=400
                )

            user.delete()

            return Response({"message": "User deleted"})

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=404
            )

        except Exception:
            print("🔥 USERS DELETE ERROR:")
            print(traceback.format_exc())

            return Response(
                {"error": "Delete failed"},
                status=500
            )
