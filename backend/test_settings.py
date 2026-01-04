from fastapi.testclient import TestClient
from main import app
import os
import json

client = TestClient(app)

def test_settings_flow():
    # 1. Get initial settings
    response = client.get("/settings")
    assert response.status_code == 200
    initial_settings = response.json()
    print(f"Initial settings: {initial_settings}")
    
    # Verify default keys exist
    assert "theme" in initial_settings
    assert "voice" in initial_settings
    assert "api_key" in initial_settings

    # 2. Update settings
    new_settings = {
        "theme": "light",
        "voice": "nova",
        "api_key": "test_key_123"
    }
    response = client.post("/settings", json=new_settings)
    assert response.status_code == 200
    updated_response = response.json()
    
    # Verify response matches update
    assert updated_response["theme"] == "light"
    assert updated_response["voice"] == "nova"
    assert updated_response["api_key"] == "test_key_123"

    # 3. Verify persistence (get again)
    response = client.get("/settings")
    assert response.status_code == 200
    persisted_settings = response.json()
    assert persisted_settings["theme"] == "light"
    assert persisted_settings["voice"] == "nova"
    
    print("Settings flow test passed!")

    # Cleanup (Reset to defaults)
    client.post("/settings", json={
        "theme": "dark",
        "voice": "default",
        "api_key": ""
    })

if __name__ == "__main__":
    test_settings_flow()
