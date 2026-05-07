# apps/payments/services.py

import requests
from django.conf import settings


def send_mobile_money_payment(order_id, phone_number, provider, amount):
    """
    Trigger Tigo Pesa / YAS (Airtel Money) payment request.
    """

    payload = {
        "amount": str(amount),
        "phone_number": phone_number,
        "order_id": str(order_id),
        "shortcode": settings.TIGO_SHORTCODE,
        "provider": provider,  # TIGO or YAS
        "callback_url": settings.TIGO_CALLBACK_URL,
    }

    headers = {
        "Authorization": f"Bearer {settings.TIGO_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            settings.TIGO_API_URL,
            json=payload,
            headers=headers,
            timeout=20
        )

        # Try to parse response safely
        try:
            data = response.json()
        except Exception:
            return {
                "success": False,
                "error": "Invalid JSON response from payment provider",
                "raw": response.text
            }

        # Check HTTP status
        if response.status_code in [200, 201]:
            return {
                "success": True,
                "data": data
            }

        return {
            "success": False,
            "status_code": response.status_code,
            "data": data
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout - payment provider not responding"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }
