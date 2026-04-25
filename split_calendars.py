import re
from pathlib import Path
from datetime import datetime, timezone

import requests
from icalendar import Calendar, Event

SOURCE_URL = "https://calendar.google.com/calendar/ical/5c9dc1a627cf55f1653d17573c2df58075d949559ec87e484b0cf90fa78bbf6d%40group.calendar.google.com/public/basic.ics"
OUTPUT_DIR = Path("public")

ATTRIBUTION = (
    "Source: INRNG Pro Cycling Calendar – https://inrng.com/calendar/ "
    "Filtered calendar generated independently."
)

FILTERS = {
    "men-worldtour.ics": {
        "name": "Cycling – Men WorldTour",
        "patterns": [r"\b1\.UWT\b", r"\b2\.UWT\b"],
    },
    "women-worldtour.ics": {
        "name": "Cycling – Women WorldTour",
        "patterns": [r"\b1\.WWT\b", r"\b2\.WWT\b"],
    },
    "worldtour-all.ics": {
        "name": "Cycling – WorldTour All",
        "patterns": [r"\b1\.UWT\b", r"\b2\.UWT\b", r"\b1\.WWT\b", r"\b2\.WWT\b"],
    },
    "one-day-rest.ics": {
        "name": "Cycling – One Day Rest",
        "patterns": [r"\b1\.(?!UWT\b|WWT\b)[A-Za-z0-9.]+\b"],
    },
    "stage-race-rest.ics": {
        "name": "Cycling – Stage Race Rest",
        "patterns": [r"\b2\.(?!UWT\b|WWT\b)[A-Za-z0-9.]+\b"],
    },
}


def matches(title: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, title) for pattern in patterns)


def clone_event(event: Event) -> Event:
    new_event = Event()
    for key, value in event.items():
        new_event[key] = value

    description = str(new_event.get("DESCRIPTION", "")).strip()
    new_event["DESCRIPTION"] = f"{description}\n\n{ATTRIBUTION}".strip()
    return new_event


def build_calendar(name: str) -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//inrng-calendar-splitter//github-pages//")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", name)
    cal.add("x-wr-caldesc", ATTRIBUTION)
    return cal


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("⬇️ Lade Kalender...")
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    print("📦 Parse Kalender...")
    source_calendar = Calendar.from_ical(response.content)
    events = [
        component
        for component in source_calendar.walk()
        if component.name == "VEVENT"
    ]

    print(f"🔢 {len(events)} Events gefunden")

    generated = {}

    for filename, config in FILTERS.items():
        cal = build_calendar(config["name"])
        count = 0

        for event in events:
            title = str(event.get("SUMMARY", ""))
            if matches(title, config["patterns"]):
                cal.add_component(clone_event(event))
                count += 1

        path = OUTPUT_DIR / filename
        path.write_bytes(cal.to_ical())

        print(f"✅ {filename}: {count} Events")

        generated[filename] = config["name"]

    index = [
        "<!doctype html>",
        "<html><head><meta charset='utf-8'><title>Cycling Calendars</title></head><body>",
        "<h1>Cycling Calendars</h1>",
        "<p>Filtered calendars based on the INRNG Pro Cycling Calendar.</p>",
        "<p>Source: <a href='https://inrng.com/calendar/'>INRNG Calendar</a></p>",
        "<ul>",
    ]

    for filename, name in generated.items():
        index.append(f"<li><a href='./{filename}'>{name}</a></li>")

    index.extend([
        "</ul>",
        f"<p>Last generated: {datetime.now(timezone.utc).isoformat()}</p>",
        "</body></html>",
    ])

    (OUTPUT_DIR / "index.html").write_text("\n".join(index), encoding="utf-8")

    print("🎉 Fertig! Dateien im /public Ordner")


if __name__ == "__main__":
    main()