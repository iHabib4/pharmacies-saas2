from ..models import Order


class OrderStatusService:

    VALID_TRANSITIONS = {
        "pending": ["confirmed", "failed"],
        "confirmed": ["packed", "failed"],
        "packed": ["in_transit", "failed"],
        "in_transit": ["completed", "failed"],
        "completed": [],
        "failed": [],
    }

    @staticmethod
    def update_status(order: Order, new_status: str):

        current = order.status

        allowed = OrderStatusService.VALID_TRANSITIONS.get(current, [])

        if new_status not in allowed:
            raise ValueError(
                f"Invalid transition: {current} → {new_status}"
            )

        order.status = new_status

        if new_status == "completed":
            from django.utils.timezone import now
            order.completed_at = now()

        order.save()

        return order
