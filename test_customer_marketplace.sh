#!/bin/bash

# -------------------------------
# UW PICO SaaS - Customer Testing
# Full CLI sequence for 3.2 Browse Marketplace
# -------------------------------

BASE_URL="http://127.0.0.1:8000"

# 1️⃣ Register a new customer
USERNAME="iAli-$(date +%s)"   # unique username based on timestamp
EMAIL="habibkham$(date +%s)@yahoo.com"
PASSWORD="YourPassword123"

echo "=== Registering Customer ==="
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/users/register/" \
-H "Content-Type: application/json" \
-d "{\"username\": \"$USERNAME\", \"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

echo "Register Response: $REGISTER_RESPONSE"

# 2️⃣ Login to get JWT access token
echo -e "\n=== Logging in Customer ==="
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login/" \
-H "Content-Type: application/json" \
-d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access'])")

echo "Access Token: $ACCESS_TOKEN"

# 3️⃣ List all pharmacies
echo -e "\n=== Listing All Pharmacies ==="
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" "$BASE_URL/api/pharmacies/" | python3 -m json.tool

# 4️⃣ Search for a medicine
SEARCH_MEDICINE="Paracetamol"
echo -e "\n=== Searching for Medicine: $SEARCH_MEDICINE ==="
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" "$BASE_URL/api/products/search/?search=$SEARCH_MEDICINE" | python3 -m json.tool

echo -e "\n✅ Customer 3.2 Browse Marketplace Test Completed!"
