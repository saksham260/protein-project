import urllib.request, re, json
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://www.muscleblaze.com/sv/muscleblaze-biozyme-performance-whey/SP-88093"
html = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15).read().decode("utf-8")

# Search for nutrition tables or tables in HTML
soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table")
print(f"Total tables in HTML: {len(tables)}")
for idx, tbl in enumerate(tables):
    rows = []
    for tr in tbl.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    if any("protein" in " ".join(r).lower() for r in rows):
        print(f"Table {idx} has protein!")
        with open("protein-etl/data/demo_catalog/mb_table.json", "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)

# Also check for nutrition text sections
nut_divs = soup.find_all(lambda tag: tag.name in ["div", "section"] and any(k in (tag.get("class", []) or []) for k in ["nutrit", "supple", "macro"]))
print(f"Nut divs: {len(nut_divs)}")
