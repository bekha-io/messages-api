import requests

for i in range(1, 1000):
    resp = requests.get("http://127.0.0.1:8000/users")
    print(resp.json())