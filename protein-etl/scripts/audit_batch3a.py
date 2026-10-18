import urllib.request, json, time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8"
}

def test_url(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            content_type = resp.headers.get("content-type", "")
            data = resp.read()
            return {"status": resp.status, "content_type": content_type, "length": len(data), "sample": data[:300].decode("utf-8", errors="ignore")}
    except Exception as e:
        return {"error": str(e)}

print("1. Bigmuscles Shopify products.json:")
print(test_url("https://bigmusclesnutrition.com/products.json?limit=10"))

print("\n2. The Whole Truth sitemap / products:")
print(test_url("https://thewholetruthfoods.com/sitemap.xml"))

print("\n3. Avvatar India products / sitemap:")
print(test_url("https://avvatarindia.com/sitemap.xml"))

print("\n4. MuscleBlaze products / sitemap:")
print(test_url("https://www.muscleblaze.com/sitemap.xml"))
