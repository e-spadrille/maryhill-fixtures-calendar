import json
from datetime import datetime
from icalendar import Calendar, Event

with open("fixtures.json", "r") as f:
    fixtures = json.load(f)

cal = Calendar()
cal.add("prodid", "-//Maryhill Fixtures//EN")
cal.add("version", "2.0")

for fixture in fixtures:
    event = Event()

    start_str = fixture["date"] + " " + fixture["time"]
    start_dt = datetime.strptime(start_str, "%d/%m/%y %H:%M")

    event.add("summary", f'{fixture["home"]} vs {fixture["away"]}')
    event.add("dtstart", start_dt)
    event.add("dtend", start_dt)  # Can be modified to add 2 hours if desired
    event.add("location", fixture["venue"])
    event.add("description", fixture["competition"])

    cal.add_component(event)

with open("maryhill-fixtures.ics", "wb") as f:
    f.write(cal.to_ical())
