import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URLs to scrape
urls = [
    "https://www.wosfl.co.uk/matchHub/922046009/-1_-1/853461137/-1/-1/-1/1/true.html",
    "https://www.wosfl.co.uk/matchHub/922046009/-1_-1/853461137/-1/-1/-1/1/true/2.html"
]

fixtures = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    match_rows = soup.select(".match-row")

    for row in match_rows:
        teams = row.select_one(".match-teams")
        date_time = row.select_one(".match-date")
        venue = row.select_one(".match-venue")

        if not (teams and date_time and venue):
            continue

        # Extract text cleanly
        teams_text = teams.get_text(strip=True)
        date_time_text = date_time.get_text(strip=True)
        venue_text = venue.get_text(strip=True)

        # Extract team names
        if "v" in teams_text:
            home_team, away_team = map(str.strip, teams_text.split("v"))
        else:
            continue  # skip malformed

        # Parse date/time
        try:
            dt = datetime.strptime(date_time_text, "%d %b %Y, %H:%M")
            iso_time = dt.isoformat()
        except ValueError:
            continue

        # Extract competition and ground
        if "@" in venue_text:
            competition, ground = map(str.strip, venue_text.split("@", 1))
        else:
            competition = venue_text.strip()
            ground = ""

        fixtures.append({
            "home_team": home_team,
            "away_team": away_team,
            "datetime": iso_time,
            "competition": competition,
            "ground": ground
        })

# Write to JSON
with open("fixtures.json", "w", encoding="utf-8") as f:
    json.dump(fixtures, f, indent=2)

print(f"✅ Extracted {len(fixtures)} fixtures")
