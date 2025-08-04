from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
from datetime import datetime

urls = [
    "https://www.wosfl.co.uk/matchHub/922046009/-1_-1/853461137/-1/-1/-1/0/true.html",
    "https://www.wosfl.co.uk/matchHub/922046009/-1_-1/853461137/-1/-1/-1/0/true/2.html"
]

fixtures = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for url in urls:
        print(f"⏳ Loading {url}")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Optional: save for debugging
        with open("debug_output.html", "w", encoding="utf-8") as f:
            f.write(html)

        rows = soup.select("tr[data-match-href]")
        print(f"🔍 Found {len(rows)} fixtures")

        for row in rows:
            try:
                cells = row.find_all("td")
                if len(cells) < 5:
                    continue

                # Date and time
                date_time_raw = cells[0].get_text(separator=" ", strip=True).replace("\xa0", " ")
                dt_parts = date_time_raw.split()
                if len(dt_parts) != 2:
                    print(f"⚠️ Skipping bad date/time format: {date_time_raw}")
                    continue
                dt_str = f"{dt_parts[0]} {dt_parts[1]}"
                try:
                    dt = datetime.strptime(dt_str, "%d/%m/%y %H:%M")
                    iso_time = dt.isoformat()
                except ValueError:
                    print(f"⚠️ Skipping unparseable datetime: {dt_str}")
                    continue

                # Home and away teams
                home_team = cells[1].get_text(strip=True)
                away_team = cells[3].get_text(strip=True)

                # Score is in the third <td> if the match has been played
                score = None
                if "highlight" in cells[2].get("class", []):
                    score = cells[2].get_text(strip=True)

                # Competition
                comp_span = cells[4].find("span", class_="bold")
                competition = comp_span.get_text(strip=True) if comp_span else ""

                # Ground
                at_text = cells[4].find_all("span")
                ground = ""
                if len(at_text) > 1:
                    ground = at_text[1].get_text(strip=True).replace("@", "").strip()

                fixtures.append({
                    "home_team": home_team,
                    "away_team": away_team,
                    "datetime": iso_time,
                    "competition": competition,
                    "ground": ground,
                    "result": score
                })

            except Exception as e:
                print(f"⚠️ Error parsing row: {e}")
                continue

    browser.close()

# Save fixtures
with open("fixtures.json", "w", encoding="utf-8") as f:
    json.dump(fixtures, f, indent=2)

print(f"✅ Extracted {len(fixtures)} fixtures")
