# apps/orders/admin.py

from datetime import datetime, timedelta

from django.contrib import admin
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from .models import Order, OrderItem


# ------------------------------
# Inline for Order Items
# ------------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price", "delivery_code")
    fields = ("product", "batch", "quantity", "price", "delivery_code")


# ------------------------------
# Date range filter for Orders
# ------------------------------
class OrderDateRangeFilter(admin.SimpleListFilter):
    title = _("Order Date Range")
    parameter_name = "date_range"

    def lookups(self, request, model_admin):
        return [
            ("today", _("Today")),
            ("last_7_days", _("Last 7 days")),
            ("last_30_days", _("Last 30 days")),
            ("this_month", _("This Month")),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        today = datetime.today()
        if value == "today":
            return queryset.filter(created_at__date=today.date())
        elif value == "last_7_days":
            start = today - timedelta(days=7)
            return queryset.filter(created_at__gte=start)
        elif value == "last_30_days":
            start = today - timedelta(days=30)
            return queryset.filter(created_at__gte=start)
        elif value == "this_month":
            return queryset.filter(
                created_at__year=today.year, created_at__month=today.month
            )
        return queryset


# ------------------------------
# Admin for Orders
# ------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "consumer",
        "pharmacy",
        "rider",
        "status",
        "total_price",
        "commission",
        "vendor_amount",
        "created_at",
        "updated_at",
    ]
    readonly_fields = [
        "id",
        "total_price",
        "commission",
        "vendor_amount",
        "created_at",
        "updated_at",
        "delivery_codes",
    ]
    list_filter = ["status", "pharmacy", "rider", OrderDateRangeFilter]
    search_fields = ["consumer__first_name", "consumer__last_name", "pharmacy__name"]
    ordering = ["-created_at"]
    inlines = [OrderItemInline]
    change_list_template = "admin/orders_change_list.html"

    def delivery_codes(self, obj):
        """
        Concatenate delivery codes from all related OrderItems.
        """
        codes = [item.delivery_code or "" for item in obj.items.all()]
        return ", ".join(codes)

    delivery_codes.short_description = "Delivery Codes"

    def changelist_view(self, request, extra_context=None):
        qs = self.get_queryset(request)
        # Aggregate summary per pharmacy
        qs_summary = (
            qs.values("pharmacy__name")
            .annotate(
                total_commission=Sum("commission"),
                total_vendor_amount=Sum("vendor_amount"),
                total_orders=Sum("total_price"),
            )
            .order_by("pharmacy__name")
        )

        extra_context = extra_context or {}
        extra_context["commission_summary"] = qs_summary
        return super().changelist_view(request, extra_context=extra_context)


# ------------------------------
# Admin for Order Items
# ------------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "product",
        "batch",
        "quantity",
        "price",
        "status",
        "delivery_code",
        "created_at",
        "completed_at",
    ]
    readonly_fields = ["id", "price", "delivery_code", "created_at", "completed_at"]
    list_filter = ["status", "product"]
    search_fields = [
        "product__name",
        "order__consumer__first_name",
        "order__consumer__last_name",
    ]
