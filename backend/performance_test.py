#!/usr/bin/env python3
import os
import random
import sys
import threading
import time

from django.db import transaction

# -----------------------------
# Django setup
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from apps.orders.models import Order
from apps.products.models import MedicineBatch as InventoryBatch
from apps.riders.models import Rider
# -----------------------------
# Import models
# -----------------------------
from apps.users.models import CustomUser as Customer

# -----------------------------
# Config
# -----------------------------
NUM_ORDERS = 200
NUM_RIDERS = 20
MAX_ITEMS_PER_ORDER = 3
NUM_THREADS = 50  # simulate 50 users

lock = threading.Lock()
results = []


# -----------------------------
# Helpers
# -----------------------------
def get_available_stock():
    return list(InventoryBatch.objects.filter(quantity__gt=0))


def place_order(customer):
    start = time.time()

    try:
        with transaction.atomic():
            batches = get_available_stock()
            if not batches:
                return None

            order = Order.objects.create(customer=customer)
            remaining = random.randint(1, MAX_ITEMS_PER_ORDER)

            for batch in batches:
                if remaining <= 0:
                    break

                take = min(batch.quantity, remaining)

                order.items.create(product=batch.product, quantity=take)

                batch.quantity -= take
                batch.save()

                remaining -= take

        latency = time.time() - start

        with lock:
            results.append(latency)

        return order

    except Exception as e:
        print(f"Error placing order: {e}")
        return None


def update_rider_locations():
    start = time.time()

    riders = Rider.objects.all()[:NUM_RIDERS]

    for rider in riders:
        rider.latitude += random.uniform(-0.001, 0.001)
        rider.longitude += random.uniform(-0.001, 0.001)
        rider.save()

    print(f"Rider updates took {round(time.time() - start, 2)}s")


# -----------------------------
# Worker thread
# -----------------------------
def worker(customers, orders_target):
    success = 0

    while success < orders_target:
        customer = random.choice(customers)
        order = place_order(customer)

        if order:
            print(f"Order #{order.id} by Customer {customer.id}")
            success += 1
        else:
            print("Order failed (no stock)")


# -----------------------------
# Main test
# -----------------------------
def run_stress_test():
    print(f"\n🚀 Starting stress test...")
    print(f"Orders: {NUM_ORDERS}, Riders: {NUM_RIDERS}, Threads: {NUM_THREADS}")

    customers = list(Customer.objects.all())

    if not customers:
        raise Exception("❌ No customers found!")

    threads = []
    orders_per_thread = NUM_ORDERS // NUM_THREADS

    start_time = time.time()

    # 🔥 Create threads (simulate users)
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(customers, orders_per_thread))
        threads.append(t)
        t.start()

    # ⏳ Wait for all threads
    for t in threads:
        t.join()

    # 🚴 Rider updates
    print("\n📍 Updating rider locations...")
    update_rider_locations()

    total_time = time.time() - start_time

    # 📊 Metrics
    if results:
        avg = sum(results) / len(results)
        print(f"\n📊 RESULTS:")
        print(f"Total orders placed: {len(results)}")
        print(f"Average response time: {round(avg, 3)}s")
        print(f"Total test time: {round(total_time, 2)}s")

    print("\n✅ Stress test completed.")


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    run_stress_test()
