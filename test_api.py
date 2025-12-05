import requests
import json

def test_verify():
    url = "http://localhost:8000/api/v1/verify"
    
    # Create a dummy file
    with open("test_doc.txt", "w") as f:
        f.write("This is a Board Consent to increase authorized shares. Signed by John Doe on 2023-01-01.")
        
    files = {
        "file": ("test_doc.txt", open("test_doc.txt", "rb"), "text/plain")
    }
    
    data = {
        "name": "Test Board Consent",
        "id": "12345",
        "workflow_type": "INCREASE_AUTHORIZED_SHARES"
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_verify()
