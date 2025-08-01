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
        soup = BeautifulSoup(res.text, 'html.parser')

        table = soup.find('table')
        if not table:
            continue

        rows = table.find_all('tr')[1:]  # skip header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 5:
                continue

            date_str = cols[0].get_text(strip=True)
            teams = cols[1].get_text(strip=True)
            time_str = cols[2].get_text(strip=True)
            comp_venue = cols[4].get_text(strip=True)

            # Clean up
            dt = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%y %H:%M")
            home, away = [t.strip() for t in teams.split('vs')]
            competition = comp_venue.split('@')[0].strip()
            location = comp_venue.split('@')[1].strip() if '@' in comp_venue else ""

            if "Maryhill" not in teams:
                continue  # Skip unrelated matches

            fixtures.append({
                "datetime": dt.isoformat(),
                "home": home,
                "away": away,
                "competition": competition,
                "location": location
            })

    return fixtures
