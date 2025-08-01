import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URLs to scrape
urls = [
    "https://www.wosfl.co.uk/matchHub/922046009/-1_-1/853461137/-1/-1/-1/1/true.html",
    "https://www.wosfl.co.uk/matchHub/922046009/-1_-1/853461137/-1/-1/-1/1/true/2.html"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

fixtures = []

for url in urls:
    response = requests.get(url, headers=headers)
    with open(f"page_{urls.index(url)+1}.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("table.table.table-striped tbody tr")

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 6:
            continue

        # Extract fields
        date_text = cells[0].get_text(strip=True)
        time_text = cells[1].get_text(strip=True)
        home_team = cells[2].get_text(strip=True)
        away_team = cells[4].get_text(strip=True)
        venue = cells[5].get_text(strip=True)
        competition = cells[6].get_text(strip=True) if len(cells) > 6 else ""

        # Merge date & time
        try:
            dt = datetime.strptime(f"{date_text} {time_text}", "%a %d %b %Y %H:%M")
            iso_time = dt.isoformat()
        except ValueError:
            continue  # skip malformed rows

        fixtures.append({
            "home_team": home_team,
            "away_team": away_team,
            "datetime": iso_time,
            "competition": competition,
            "ground": venue
        })

# Write to JSON
with open("fixtures.json", "w", encoding="utf-8") as f:
    json.dump(fixtures, f, indent=2)

print(f"✅ Extracted {len(fixtures)} fixtures")
