from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# =========================================================
# CUSTOM USER MANAGER
# =========================================================
class CustomUserManager(BaseUserManager):

    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("Mobile number is required")

        mobile_number = str(mobile_number).strip()

        user = self.model(
            mobile_number=mobile_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        return self.create_user(
            mobile_number,
            password,
            **extra_fields
        )


# =========================================================
# CUSTOM USER MODEL
# =========================================================
class CustomUser(AbstractUser):

    # Remove username completely
    username = None

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("customer", "Customer"),
        ("pharmacy", "Pharmacy"),
        ("rider", "Rider"),
        ("supplier", "Supplier"),
    )

    # Authentication field
    mobile_number = models.CharField(
        max_length=15,
        unique=True
    )

    # RBAC role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    # Pharmacy assignment
    pharmacy = models.OneToOneField(
        "pharmacies.Pharmacy",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_user"
    )

    # Profile image
    profile_picture = models.ImageField(
        upload_to="profiles/",
        null=True,
        blank=True
    )

    # Status flags
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Login field
    USERNAME_FIELD = "mobile_number"

    REQUIRED_FIELDS = []

    # Manager
    objects = CustomUserManager()

    class Meta:
        db_table = "users"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.mobile_number} ({self.role})"

    # =====================================================
    # RBAC HELPERS
    # =====================================================
    @property
    def is_admin(self):
        return (
            self.role == "admin"
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_pharmacy(self):
        return self.role == "pharmacy"

    @property
    def is_customer(self):
        return self.role == "customer"

    @property
    def is_rider(self):
        return self.role == "rider"

    @property
    def is_supplier(self):
        return self.role == "supplier"


# =========================================================
# AUDIT LOG
# =========================================================
class AuditLog(models.Model):

    actor = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actor_logs"
    )

    action = models.CharField(
        max_length=255
    )

    target_user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="target_logs"
    )

    metadata = models.JSONField(
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "audit_logs"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.actor} -> {self.action}"
