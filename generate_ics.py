import json
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz

uk_tz = pytz.timezone("Europe/London")

with open("fixtures.json", "r", encoding="utf-8") as f:
    fixtures = json.load(f)

cal = Calendar()

for fixture in fixtures:
    try:
        dt = datetime.fromisoformat(fixture["datetime"])
        dt = uk_tz.localize(dt)

        event = Event()
        event.name = f"{fixture['home_team']} vs {fixture['away_team']}"
        event.begin = dt
        event.end = dt + timedelta(minutes=105)

        # Description includes competition and result (if present)
        description_lines = [f"{fixture['competition']}"]
        if fixture.get("result"):
            description_lines.append(f"Result: {fixture['result']}")
        event.description = "\n".join(description_lines)

        # Location is the ground (if present)
        if fixture.get("ground"):
            event.location = fixture["ground"]

        cal.events.add(event)

    except Exception as e:
        print(f"⚠️ Skipping event due to error: {e}")
        continue

with open("maryhill-fixtures.ics", "w", encoding="utf-8") as f:
    f.writelines(cal)

print(f"✅ Generated maryhill-fixtures.ics with {len(cal.events)} events")
