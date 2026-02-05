import requests
import sys
from config import Config

def check_health():
    print(f"Testing connection to Endee at: {Config.ENDEE_URL}")
    try:
        response = requests.get(f"{Config.ENDEE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Endee server is UP and REACHABLE!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ FAILED to connect. Check if:")
        print(f"   1. The Endee server is running on {Config.ENDEE_HOST}")
        print(f"   2. Port {Config.ENDEE_PORT} is open in your Mac's firewall")
        print(f"   3. Both devices are on the same network")
        return False
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return False

if __name__ == "__main__":
    if not check_health():
        sys.exit(1)
