# apps/payments/services.py
import requests
from django.conf import settings


def send_mobile_money_payment(order_id, phone_number, provider, amount):
    """
    Trigger Tigo Pesa payment request.
    """
    payload = {
        "amount": amount,
        "phone_number": phone_number,
        "order_id": order_id,
        "shortcode": settings.TIGO_SHORTCODE,
        "provider": provider,
        "callback_url": settings.TIGO_CALLBACK_URL,
    }

    headers = {
        "Authorization": f"Bearer {settings.TIGO_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(settings.TIGO_API_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
