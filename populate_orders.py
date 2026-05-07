# populate_orders.py
import os
import django
import random

# 1. Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # correct path
django.setup()

# 2. Imports
from django.contrib.auth import get_user_model
from apps.orders.models import Order, OrderItem
from apps.deliveries.models import Delivery
from apps.pharmacies.models import Pharmacy
from apps.products.models import Product

# 3. Constants
NUM_ORDERS = 30
ORDER_STATUSES = ["pending", "processing", "completed", "cancelled"]
PAYMENT_STATUSES = ["unpaid", "paid", "refunded"]
PAYMENT_PROVIDERS = ["cash", "card", "wallet"]

# 4. Query sets
User = get_user_model()
customers = list(User.objects.filter(role="customer"))
riders = list(User.objects.filter(role="rider"))
pharmacies = list(Pharmacy.objects.all())
products = list(Product.objects.all())

# 5. Fallbacks
if not customers:
    print("No customers found. Exiting.")
    exit()
if not pharmacies:
    print("No pharmacies found. Exiting.")
    exit()
if not products:
    print("No products found. Exiting.")
    exit()

# 6. Create orders
orders_created = []

for _ in range(NUM_ORDERS):
    customer = random.choice(customers)
    pharmacy = random.choice(pharmacies)
    delivery_address = f"{customer.username} address"

    order_status = random.choice(ORDER_STATUSES)
    payment_status = random.choice(PAYMENT_STATUSES)
    payment_provider = random.choice(PAYMENT_PROVIDERS)

    order = Order.objects.create(
        consumer=customer,
        pharmacy=pharmacy,
        delivery_address=delivery_address,
        status=order_status,
        payment_status=payment_status,
        payment_provider=payment_provider,
        total_price=0,
        commission=0,
        vendor_amount=0
    )

    total_price = 0
    for _ in range(random.randint(1, 5)):
        product = random.choice(products)
        quantity = random.randint(1, 3)
        price = getattr(product, "price", 1000)
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
        total_price += price * quantity

    order.total_price = total_price
    order.vendor_amount = total_price * 0.85
    order.commission = total_price * 0.15
    order.save()

    if riders:
        rider_user = random.choice(riders)
        rider_instance = getattr(rider_user, 'rider', None)  # safe fallback
        if rider_instance:
            order.rider = rider_instance
            order.save()
            Delivery.objects.create(order=order, rider=rider_instance)

    orders_created.append(order)

print(f"Orders created: {len(orders_created)}")
