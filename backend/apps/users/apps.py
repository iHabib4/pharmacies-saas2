# apps/users/apps.py

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the 'users' app.

    Attributes:
        default_auto_field (str): The default primary key type for models.
        name (str): Full Python path to the app folder.
        label (str, optional): Optional unique label for the app.
    """

    # Use BigAutoField as default for all models' primary keys
    default_auto_field = "django.db.models.BigAutoField"

    # Full Python path to the app
    name = "apps.users"  # ✅ Must match folder structure

    # Optional: only use if another app named 'users' exists
    # This avoids "Application labels aren't unique" errors
    # label = 'custom_users'

    def ready(self):
        """
        Called when the app is fully loaded.
        Import signals here so they are registered at startup.
        """
        # Ensure signals are imported and registered
        import apps.users.signals  # noqa: F401
