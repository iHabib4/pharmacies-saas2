# apps/users/signals.py

from django.contrib.auth import get_user_model  # <-- use this
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# Get the currently active user model
User = get_user_model()


@receiver(post_save, sender=User)
def assign_customer_role(sender, instance, created, **kwargs):
    """
    Automatically assign the 'Customer' group to newly registered users.
    """
    if created:  # Only for new users
        try:
            customer_group = Group.objects.get(name="Customer")
        except Group.DoesNotExist:
            # Create the group if it doesn't exist
            customer_group = Group.objects.create(name="Customer")

        instance.groups.add(customer_group)
