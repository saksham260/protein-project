"""Find real URLs and APIs for Batch 4C brands."""
import httpx
from bs4 import BeautifulSoup

candidates = [
    "fuelone.in",
    "www.fuelone.in",
    "kapiva.in",
    "www.kapiva.in",
    "boltnutrition.in",
    "www.boltnutrition.in",
    "boltnutrition.com",
    "xlr8.co.in",
    "xlr8nutrition.in",
    "www.xlr8nutrition.in",
    "xlr8sportsnutrition.com"
]

client = httpx.Client(follow_redirects=True, timeout=10, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"})

for d in candidates:
    for proto in ["https://"]:
        url = f"{proto}{d}"
        try:
            r = client.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
            print(f"[OK] {d} -> {r.status_code} | Final: {r.url} | Title: {title[:50]}")
        except Exception as e:
            print(f"[FAIL] {d}: {str(e)[:60]}")
