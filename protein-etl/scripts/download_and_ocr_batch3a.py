import urllib.request, json, re, io, os
from pathlib import Path
from PIL import Image
from rapidocr import RapidOCR

ocr = RapidOCR()
LABELS_DIR = Path("protein-etl/data/demo_catalog/labels")
LABELS_DIR.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_bytes(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def fetch_html(url):
    data = fetch_bytes(url)
    return data.decode("utf-8", errors="ignore") if data else ""

print("Downloading & auditing images for Batch 3A...")
