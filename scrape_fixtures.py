import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.wosfl.co.uk"
PAGES = [
    "/matchHub/922046009/-1_-1/853461137/-1/-1/-1/1/true.html",
    "/matchHub/922046009/-1_-1/853461137/-1/-1/-1/1/true/2.html",
]

fixtures = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

for page in PAGES:
    url = BASE_URL + page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Save page contents to help debug
    with open("debug.html", "w") as f:
        f.write(response.text)

    rows = soup.select("div.matchHub__row")

    for row in rows:
        try:
            date_time = row.select_one(".matchHub__datetime").get_text(strip=True).split()
            date = date_time[0]
            time = date_time[1] if len(date_time) > 1 else "14:00"

            teams = row.select(".matchHub__teamTitle")
            if len(teams) != 2:
                continue
            home = teams[0].get_text(strip=True)
            away = teams[1].get_text(strip=True)

            competition = row.select_one(".matchHub__gameInfo").get_text(strip=True)
            venue = row.select_one(".matchHub__gameInfo + div").get_text(strip=True).replace("@", "").strip()

            fixtures.append({
                "date": date,
                "time": time,
                "home": home,
                "away": away,
                "competition": competition,
                "venue": venue
            })
        except Exception as e:
            print("Skipping row due to error:", e)

# Output number of fixtures scraped
print(f"Scraped {len(fixtures)} fixtures")

with open("fixtures.json", "w") as f:
    json.dump(fixtures, f, indent=2)
