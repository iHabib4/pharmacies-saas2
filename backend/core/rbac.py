ROLE_PERMISSIONS = {
    "admin": ["*"],
    "pharmacy_owner": ["manage_stock", "view_orders"],
    "supplier": ["view_orders"],
    "rider": ["update_delivery_status"],
    "customer": ["place_order"]
}


def has_permission(user, permission):
    perms = ROLE_PERMISSIONS.get(user.role, [])
    return "*" in perms or permission in perms


def is_admin(user):
    return user.role == "admin"
