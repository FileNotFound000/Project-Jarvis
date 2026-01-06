import requests
import json

url = "http://localhost:8000/chat"
data = {
    "message": "research history of python programming",
    "session_id": "test_session"
}

print(f"Sending request to {url}...")
try:
    with requests.post(url, data=data, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    json_str = decoded_line[6:]
                    try:
                        data = json.loads(json_str)
                        if "text" in data:
                            print(data["text"], end="", flush=True)
                        if "command" in data:
                            print(f"\nCOMMAND: {data['command']}")
                    except json.JSONDecodeError:
                        print(f"\nRaw data: {decoded_line}")
except Exception as e:
    print(f"Error: {e}")
