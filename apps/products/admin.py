from django.contrib import admin
from .models import Product, MedicineBatch


# =========================
# INLINE FOR BATCHES
# =========================
class MedicineBatchInline(admin.TabularInline):
    model = MedicineBatch
    extra = 1
    fields = ("pharmacy", "batch_number", "price", "quantity")
    show_change_link = True


# =========================
# PRODUCT ADMIN
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [MedicineBatchInline]


# =========================
# BATCH ADMIN
# =========================
@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "pharmacy",
        "batch_number",
        "price",
        "quantity",
    )
    list_filter = ("pharmacy", "product")
    search_fields = ("product__name", "pharmacy__name", "batch_number")
