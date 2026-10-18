import urllib.request
import json

token = "6ad4db47c9a14bd554a77978"
url = "https://shop.amul.com/api/1.1/entity/ms.products?limit=10"

headers_to_try = [
    {"User-Agent": "Mozilla/5.0", "token": token},
    {"User-Agent": "Mozilla/5.0", "x-token": token},
    {"User-Agent": "Mozilla/5.0", "Authorization": f"Bearer {token}"},
    {"User-Agent": "Mozilla/5.0", "x-csrf-token": token},
    {"User-Agent": "Mozilla/5.0", "Cookie": f"token={token}; tid=u6vndngyl9"},
    {"User-Agent": "Mozilla/5.0", "ms-token": token},
    {"User-Agent": "Mozilla/5.0", "auth-token": token}
]

for idx, h in enumerate(headers_to_try):
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=8) as r:
            print(f"Header {idx} SUCCESS! Status: {r.status}")
            data = json.loads(r.read())
            print("Items:", len(data.get("data", [])))
            break
    except Exception as e:
        print(f"Header {idx} failed:", e)
