import requests
import json

# Configuration
PIHOLE_IP = "<pi-hole-ip-address>"  # Replace with your Pi-hole IP address
PASSWORD = "<pi-hole-password>"   # Replace with your Pi-hole password

def enable_pihole_blocking():
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

        # Step 2: Enable blocking
        blocking_url = f"http://{PIHOLE_IP}/api/dns/blocking"
        headers = {"sid": sid}
        blocking_payload = {"blocking": True}

        response = requests.post(blocking_url, json=blocking_payload, headers=headers, timeout=5)

        if response.status_code == 200:
            print("Pi-hole blocking enabled successfully")
        else:
            print(f"Failed to enable blocking: {response.status_code}")

        # Step 3: Logout (optional but recommended)
        logout_response = requests.delete(auth_url, headers=headers, timeout=5)
        if logout_response.status_code == 200:
            print("Successfully logged out")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    enable_pihole_blocking()
