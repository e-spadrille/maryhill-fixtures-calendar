import requests
from bs4 import BeautifulSoup
from datetime import datetime

PAGES = [
    "https://www.wosfl.co.uk/matchHub/922046009/-1_-1/853461137/-1/-1/-1/1/true.html",
    "https://www.wosfl.co.uk/matchHub/922046009/-1_-1/853461137/-1/-1/-1/1/true/2.html"
]

def fetch_fixtures():
    fixtures = []

    for url in PAGES:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        rows = soup.select("table tbody tr")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 5:
                continue

            datetime_str = cells[0].get_text(strip=True)
            teams_html = cells[1]
            comp_venue_text = cells[4].get_text(strip=True)

            try:
                date_part, time_part = datetime_str.split()
                dt = datetime.strptime(f"{date_part} {time_part}", "%d/%m/%y %H:%M")
            except ValueError:
                continue

            teams = teams_html.get_text(" ", strip=True).split(" vs ")
            if len(teams) != 2:
                continue

            home, away = teams
            if "Maryhill" not in (home + away):
                continue

            if "@" in comp_venue_text:
                competition, location = comp_venue_text.split("@", 1)
            else:
                competition = comp_venue_text
                location = ""

            fixtures.append({
                "datetime": dt.isoformat(),
                "home": home.strip(),
                "away": away.strip(),
                "competition": competition.strip(),
                "location": location.strip()
            })

    return fixtures
