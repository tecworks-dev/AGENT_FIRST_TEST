# debug_test_routes.py

import requests
import json
from datetqqqqime import datetime

BASE_URL = "http://localhost:5000"  # Adjust this if your server runs on a different port

def test_route(method, route, data=None, files=None):
    url = f"{BASE_URL}{route}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, files=files)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            return f"Unsupported method: {method}"

        return {
            "status_code": response.status_code,
            "content": response.text,
            "headers": dict(response.headers)
        }
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def run_tests():
    tests = [
        ("GET", "/"),
        ("POST", "/register", {"username": "testuser", "password": "testpass"}),
        ("POST", "/login", {"username": "testuser", "password": "testpass"}),
        ("POST", "/messages", {"sender_id": 1, "receiver_id": 2, "content": "Test message"}),
        ("GET", "/messages/1"),
        ("PUT", "/messages/1", {"content": "Updated test message"}),
        ("DELETE", "/messages/1"),
        ("POST", "/media", None, {"file": ("test.txt", b"Test file content")}),
        ("GET", "/media/1"),
        ("DELETE", "/media/1"),
        ("GET", "/search?query=test"),
    ]

    results = []
    for method, route, *args in tests:
        print(f"Testing {method} {route}...")
        result = test_route(method, route, *args)
        results.append({"method": method, "route": route, "result": result})

    return results

def generate_report(results):
    report = []
    report.append("Debugging Diagnostic Test Report")
    report.append(f"Generated at: {datetime.now()}")
    report.append("=" * 50)

    for test in results:
        report.append(f"\nTesting {test['method']} {test['route']}")
        result = test['result']
        
        if isinstance(result, str):
            report.append(f"Error: {result}")
        else:
            report.append(f"Status Code: {result['status_code']}")
            if result['status_code'] >= 400:
                report.append("Unexpected Response:")
                report.append(f"Content: {result['content']}")
            report.append("Headers:")
            for key, value in result['headers'].items():
                report.append(f"  {key}: {value}")

        report.append("-" * 50)

    return "\n".join(report)

if __name__ == "__main__":
    print("Running diagnostic tests...")
    results = run_tests()
    report = generate_report(results)
    
    print("\nTest Report:")
    print(report)

    # Save report to file
    with open("diagnostic_report.txt", "w") as f:
        f.write(report)
    
    print("\nReport saved to diagnostic_report.txt")
