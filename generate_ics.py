from datetime import datetime, timedelta
import json

def create_ics(fixtures):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "PRODID:-//Maryhill Fixtures//EN"
    ]

    for f in fixtures:
        dt = datetime.fromisoformat(f["datetime"])
        dt_end = dt + timedelta(hours=2)

        lines += [
            "BEGIN:VEVENT",
            f"DTSTART;TZID=Europe/London:{dt.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND;TZID=Europe/London:{dt_end.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{f['home']} vs {f['away']}",
            f"LOCATION:{f['location']}",
            f"DESCRIPTION:{f['competition']}",
            "END:VEVENT"
        ]

    lines.append("END:VCALENDAR")
    return "\n".join(lines)

if __name__ == "__main__":
    from scrape_fixtures import fetch_fixtures

    fixtures = fetch_fixtures()
    with open("maryhill-fixtures.ics", "w") as f:
        f.write(create_ics(fixtures))

    # Optional: save a readable copy of the fixtures for debugging
    with open("fixtures.json", "w") as f:
        json.dump(fixtures, f, indent=2)
