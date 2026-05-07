# apps/users/signals.py

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def assign_customer_role(sender, instance, created, **kwargs):
    """
    Automatically assign the 'Customer' group to newly registered users.
    Safe version: does NOT create groups inside signals.
    """

    if not created:
        return

    try:
        # Only fetch existing group
        customer_group = Group.objects.get(name="Customer")
    except Group.DoesNotExist:
        # Do NOT create groups inside signals (prevents admin/migration crashes)
        return

    # Assign user to group
    instance.groups.add(customer_group)
