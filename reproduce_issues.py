import requests
import json
import sseclient


def test_sse_post_405():
    print("\n--- Testing POST /sse (Expect 400, checking for 405) ---")
    try:
        response = requests.post(
            "http://127.0.0.1:8000/sse",
            json={"jsonrpc": "2.0", "method": "initialize", "id": 1},
        )
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
        if response.status_code == 405:
            print("FAIL: Got 405 Method Not Allowed (Route ordering issue confirmed)")
        elif response.status_code == 400:
            print("PASS: Got 400 Bad Request (Custom route working)")
        else:
            print(f"Unknown status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


def test_endpoint_slash():
    print("\n--- Testing SSE Endpoint Slash (Expect trailing slash) ---")
    try:
        messages = sseclient.SSEClient("http://127.0.0.1:8000/sse")
        for msg in messages:
            if msg.event == "endpoint":
                print(f"Received endpoint event: {msg.data}")
                if "?" in msg.data:
                    path = msg.data.split("?")[0]
                    if not path.endswith("/"):
                        print(
                            "FAIL: Endpoint URL missing trailing slash (Causes 307 Redirect)"
                        )
                    else:
                        print("PASS: Endpoint URL has trailing slash")
                break
    except Exception as e:
        print(f"Error connecting to SSE: {e}")


if __name__ == "__main__":
    test_sse_post_405()
    test_endpoint_slash()
