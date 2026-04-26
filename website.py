from datetime import datetime, timezone


def build_website(filters: dict) -> str:
    generated_at = datetime.now(timezone.utc).isoformat()

    cards = "\n".join(
        f"""
        <article class="card">
          <div>
            <h2>{config["name"]}</h2>
            <p>{config["description"]}</p>
          </div>

          <div class="actions">
            <a href="./{filename}">Open calendar</a>
            <button onclick="copyLink('{filename}')">Copy .ics link</button>
          </div>
        </article>
        """
        for filename, config in filters.items()
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cycling Race Calendars</title>
  <style>
    :root {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #111;
      background: #fff;
    }}

    body {{
      margin: 0;
      padding: 48px 20px;
    }}

    main {{
      max-width: 820px;
      margin: 0 auto;
    }}

    header {{
      margin-bottom: 36px;
    }}

    h1 {{
      margin: 0 0 12px;
      font-size: clamp(2rem, 6vw, 4rem);
      line-height: 1;
      letter-spacing: -0.06em;
    }}

    .intro {{
      max-width: 640px;
      color: #555;
      font-size: 1rem;
      line-height: 1.6;
    }}

    .grid {{
      display: grid;
      gap: 12px;
    }}

    .card {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      align-items: center;
      border: 1px solid #ddd;
      border-radius: 16px;
      padding: 18px;
      background: #fff;
    }}

    h2 {{
      margin: 0 0 6px;
      font-size: 1.05rem;
    }}

    p {{
      margin: 0;
    }}

    .card p {{
      color: #666;
      line-height: 1.5;
    }}

    .actions {{
      display: flex;
      gap: 8px;
      flex-shrink: 0;
    }}

    a, button {{
      border: 1px solid #111;
      border-radius: 999px;
      padding: 8px 12px;
      background: #fff;
      color: #111;
      font: inherit;
      font-size: 0.9rem;
      text-decoration: none;
      cursor: pointer;
    }}

    a:hover, button:hover {{
      background: #111;
      color: #fff;
    }}

    footer {{
      margin-top: 32px;
      color: #666;
      font-size: 0.9rem;
      line-height: 1.6;
    }}

    footer a {{
      border: 0;
      padding: 0;
      text-decoration: underline;
    }}

    @media (max-width: 680px) {{
      .card {{
        display: block;
      }}

      .actions {{
        margin-top: 14px;
        flex-wrap: wrap;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Cycling Race Calendars</h1>
      <p class="intro">
        Minimal filtered iCal feeds based on the INRNG Pro Cycling Calendar.
        Subscribe to the race categories you actually want.
      </p>
    </header>

    <section class="grid">
      {cards}
    </section>

    <footer>
      <p>
        Source:
        <a href="https://inrng.com/calendar/">INRNG Pro Cycling Calendar</a>.
        Filtered independently.
      </p>
      <p>Last generated: {generated_at}</p>
    </footer>
  </main>

  <script>
    async function copyLink(filename) {{
      const url = new URL(filename, window.location.href).href;
      await navigator.clipboard.writeText(url);
    }}
  </script>
</body>
</html>
"""