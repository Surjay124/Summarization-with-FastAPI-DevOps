import sys
import os

# Ensure we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

def test_history():
    print("Testing GET /history...")
    with TestClient(app) as client:
        response = client.get("/api/v1/history")
        
    if response.status_code == 200:
        logs = response.json()
        print(f"✅ Success! Retrieved {len(logs)} logs.")
        if logs:
            print("Sample Log:")
            print(logs[0])
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_history()
