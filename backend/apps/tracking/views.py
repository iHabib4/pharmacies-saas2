from django.shortcuts import render
# Create your views here.
from rest_framework import generics

from .models import RiderLocation
from .serializers import RiderLocationSerializer


class UpdateLocationView(generics.CreateAPIView):

    queryset = RiderLocation.objects.all()

    serializer_class = RiderLocationSerializer
