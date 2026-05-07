import random
from django.contrib.auth import get_user_model
from faker import Faker

from pharmacies.models import Pharmacy
from products.models import Product
from orders.models import Order, OrderItem
from deliveries.models import Delivery

fake = Faker()
User = get_user_model()

def run():

    print("🚀 Seeding full system...")

    # ---------------------------
    # 1. GET USERS
    # ---------------------------
    admins = User.objects.filter(role="admin")
    customers = User.objects.filter(role="customer")
    riders = User.objects.filter(role="rider")

    # ---------------------------
    # 2. CREATE PHARMACIES
    # ---------------------------
    pharmacies = []

    for admin in admins:
        pharmacy = Pharmacy.objects.create(
            name=fake.company(),
            owner=admin,
            address=fake.address(),
        )
        pharmacies.append(pharmacy)

    print(f"✅ Created {len(pharmacies)} pharmacies")

    # ---------------------------
    # 3. CREATE PRODUCTS
    # ---------------------------
    products = []

    for pharmacy in pharmacies:
        for _ in range(10):  # 10 products per pharmacy
            product = Product.objects.create(
                name=fake.word().capitalize() + " Medicine",
                description=fake.sentence(),
                price=random.randint(500, 20000),
                stock=random.randint(10, 100),
                pharmacy=pharmacy,
            )
            products.append(product)

    print(f"✅ Created {len(products)} products")

    # ---------------------------
    # 4. CREATE ORDERS
    # ---------------------------
    orders = []

    for _ in range(50):
        customer = random.choice(customers)
        pharmacy = random.choice(pharmacies)

        order = Order.objects.create(
            customer=customer,
            pharmacy=pharmacy,
            status="pending",
            total_amount=0
        )

        total = 0

        # add items
        for _ in range(random.randint(1, 3)):
            product = random.choice(products)
            quantity = random.randint(1, 5)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            total += product.price * quantity

        order.total_amount = total
        order.save()

        orders.append(order)

    print(f"✅ Created {len(orders)} orders")

    # ---------------------------
    # 5. CREATE DELIVERIES
    # ---------------------------
    deliveries = []

    for order in orders:
        rider = random.choice(riders)

        delivery = Delivery.objects.create(
            order=order,
            rider=rider,
            status="assigned"
        )

        deliveries.append(delivery)

    print(f"✅ Created {len(deliveries)} deliveries")

    print("🎉 DONE! Full system seeded.")
