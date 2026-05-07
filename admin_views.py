from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import CustomUser as User

class AdminDashboardAPIView(APIView):
    def get(self, request):
        return Response({
            "total_users": User.objects.count(),
            "customers": User.objects.filter(role="customer").count(),
            "riders": User.objects.filter(role="rider").count(),
            "pharmacies": User.objects.filter(role="pharmacy").count(),
            "suppliers": User.objects.filter(role="supplier").count(),
        })
