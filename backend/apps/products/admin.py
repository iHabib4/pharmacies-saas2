# apps/products/admin.py

from django.contrib import admin

from .models import MedicineBatch, Pharmacy, Product


@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "pharmacy",
        "batch_number",
        "price",
        "quantity",
    )  # remove expiry_date
    list_filter = ("pharmacy", "product")  # optional filters
    search_fields = ("product__name", "pharmacy__name", "batch_number")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description")  # only fields in Product
    search_fields = ("name",)


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_open",
        "latitude",
        "longitude",
        "estimated_delivery_time",
    )
    list_filter = ("is_open",)
    search_fields = ("name",)
