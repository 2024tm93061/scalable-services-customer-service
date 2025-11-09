import requests

BASE = "http://localhost:8000"

r = requests.get(f"{BASE}/customers/")
print("list:", r.status_code, r.json()[:2])

r = requests.post(f"{BASE}/customers/", json={"name":"cli-test","email":"cli-test@example.com"})
print("create:", r.status_code, r.json())

cid = r.json().get("customer_id")
r = requests.put(f"{BASE}/customers/{cid}", json={"kyc_status":"VERIFIED"})
print("update:", r.status_code, r.json())

r = requests.get(f"{BASE}/customers/{cid}")
print("get:", r.status_code, r.json())

r = requests.delete(f"{BASE}/customers/{cid}")
print("delete:", r.status_code, r.json())