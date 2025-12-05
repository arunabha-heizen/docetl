import requests
import json

def test_verify():
    url = "http://localhost:8000/api/v1/verify"
    
    # Use the provided PDF file
    pdf_filename = "Board_Consent_-_SAFE_Repurchase_-_himanshu_himanshu2.pdf"
    
    files = {
        "file": (pdf_filename, open(pdf_filename, "rb"), "application/pdf")
    }
    
    data = {
        "name": "Test Board Consent",
        "id": "12345",
        "workflow_type": "SAFE_REPURCHASE"
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        response_json = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response_json, indent=2)}")
        
        with open("test_output.json", "w") as f:
            json.dump(response_json, f, indent=2)
        print("Logged response to test_output.json")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_verify()
