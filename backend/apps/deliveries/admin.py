# apps/deliveries/admin.py

from django.contrib import admin

from .models import Delivery, Payment

admin.site.register(Delivery)
admin.site.register(Payment)
