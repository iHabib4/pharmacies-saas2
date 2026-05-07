import requests

FLUTTERWAVE_SECRET = "your-secret-key"


def initiate_mobile_payment(phone, amount, order_id):

    url = "https://api.flutterwave.com/v3/charges?type=mobile_money_tanzania"

    headers = {"Authorization": f"Bearer {FLUTTERWAVE_SECRET}"}

    payload = {
        "tx_ref": f"order_{order_id}",
        "amount": amount,
        "currency": "TZS",
        "network": "vodacom",
        "email": "customer@email.com",
        "phone_number": phone,
        "fullname": "Customer Name",
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
