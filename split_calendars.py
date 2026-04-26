import re
from pathlib import Path

import requests
from icalendar import Calendar, Event
from website import build_website

from config import SOURCE_URL, ATTRIBUTION, FILTERS
OUTPUT_DIR = Path("public")


def matches(title: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, title) for pattern in patterns)


def clone_event(event: Event) -> Event:
    new_event = Event()
    for key, value in event.items():
        new_event[key] = value

    description = str(new_event.get("DESCRIPTION", "")).strip()
    new_event["DESCRIPTION"] = f"{description}\n\n{ATTRIBUTION}".strip()
    return new_event


def build_calendar(name: str, description: str) -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//inrng-calendar-splitter//github-pages//")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", name)
    cal.add("x-wr-caldesc", f"{description} {ATTRIBUTION}")
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
        cal = build_calendar(config["name"], config.get("description", ""))
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

    html = build_website(FILTERS)
    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")

    print("🎉 Fertig! Dateien im /public Ordner")


if __name__ == "__main__":
    main()