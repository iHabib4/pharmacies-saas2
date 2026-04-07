from apps.users.models import CustomUser, Wallet


def distribute_funds(order):
    """
    Distribute funds to pharmacy and rider wallets after delivery.
    Your commission stays in the platform automatically.
    """
    if order.is_settled:
        return

    # Ensure wallets exist
    pharmacy_wallet, _ = Wallet.objects.get_or_create(user=order.pharmacy)
    rider_wallet, _ = Wallet.objects.get_or_create(user=order.rider)

    # Add funds
    pharmacy_wallet.balance += order.pharmacy_amount
    rider_wallet.balance += order.rider_amount

    pharmacy_wallet.save()
    rider_wallet.save()

    order.is_settled = True
    order.save()
