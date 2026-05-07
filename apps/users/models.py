from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

profile_picture = models.ImageField(
    upload_to="profiles/",
    null=True,
    blank=True
)

# =========================
# MANAGER
# =========================
class CustomUserManager(BaseUserManager):

    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("Mobile number is required")

        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        return self.create_user(mobile_number, password, **extra_fields)


# =========================
# USER MODEL
# =========================
class CustomUser(AbstractUser):

    username = None

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("customer", "Customer"),
        ("pharmacy", "Pharmacy"),
        ("rider", "Rider"),
        ("supplier", "Supplier"),
    )

    mobile_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")

    pharmacy = models.OneToOneField(
        "pharmacies.Pharmacy",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.mobile_number} ({self.role})"


# =========================
# AUDIT LOG
# =========================
class AuditLog(models.Model):

    actor = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="actor_logs"
    )

    action = models.CharField(max_length=255)

    target_user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="target_logs"
    )

    metadata = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} - {self.action}"
