# DISABLE PI-HOLE BLOCKING FOR 30S
import requests
import json
import time

# Configuration
PIHOLE_IP = "pi-hole-ip-address"  # Replace with your Pi-hole IP
PASSWORD = "pi-hole-password"   # Replace with your Pi-hole password

def disable_pihole_blocking():
    try:
        # Step 1: Authenticate and get session ID
        auth_url = f"http://{PIHOLE_IP}/api/auth"
        auth_payload = {"password": PASSWORD}

        response = requests.post(auth_url, json=auth_payload, timeout=5)

        if response.status_code == 200:
            session_data = response.json()
            sid = session_data["session"]["sid"]
            print(f"Authentication successful. Session ID: {sid}")
        else:
            print(f"Authentication failed: {response.status_code}")
            return

        # Step 2: Disable blocking for 30 seconds
        blocking_url = f"http://{PIHOLE_IP}/api/dns/blocking"
        headers = {"sid": sid}
        blocking_payload = {"blocking": False, "timer": 30}

        response = requests.post(blocking_url, json=blocking_payload, headers=headers, timeout=5)

        if response.status_code == 200:
            print("Pi-hole blocking disabled for 30 seconds")
        else:
            print(f"Failed to disable blocking: {response.status_code}")

        # Step 3: Logout (optional but recommended)
        logout_response = requests.delete(auth_url, headers=headers, timeout=5)
        if logout_response.status_code == 200:
            print("Successfully logged out")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    disable_pihole_blocking()
