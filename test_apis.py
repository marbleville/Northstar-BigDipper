#!/usr/bin/env python3
"""
Test script to verify API integration for the traveler page.
Run this to check if all APIs are working correctly.
"""

import requests
import json

API_BASE = "http://web-api:4000"
TRAVELER_ID = 1
TRIP_ID = 1

def test_api(endpoint, method='GET', data=None):
    """Test an API endpoint"""
    url = f"{API_BASE}{endpoint}"
    print(f"\n🧪 Testing {method} {endpoint}")

    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success - {len(data) if isinstance(data, list) else 'data'} returned")
            if isinstance(data, list) and len(data) > 0:
                print(f"   Sample: {data[0]}")
            elif isinstance(data, dict):
                print(f"   Keys: {list(data.keys())}")
            return True
        else:
            print(f"   ❌ Failed: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🚀 Testing Traveler Page API Integration")
    print("=" * 50)

    tests = [
        # Trip data
        (f"/trips/{TRIP_ID}", "GET"),

        # Itinerary
        (f"/trips/{TRIP_ID}/itinerary", "GET"),

        # Traveler notifications
        (f"/travelers/{TRAVELER_ID}/notifications", "GET"),

        # Traveler preferences
        (f"/trips/{TRIP_ID}/travelers/{TRAVELER_ID}/preferences", "GET"),

        # Trip votes
        (f"/trips/{TRIP_ID}/votes", "GET"),

        # Listings for browsing
        ("/listings", "GET"),

        # Test posting a vote (if listings exist)
        (f"/trips/{TRIP_ID}/votes", "POST", {"traveler_id": TRAVELER_ID, "listing_id": 1, "vote_value": 1}),
    ]

    passed = 0
    total = len(tests)

    for endpoint, method, *data in tests:
        if test_api(endpoint, method, data[0] if data else None):
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All APIs are working! Traveler page should function correctly.")
    else:
        print("⚠️  Some APIs failed. Check the logs and database connection.")

if __name__ == "__main__":
    main()