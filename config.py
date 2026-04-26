SOURCE_URL = "https://calendar.google.com/calendar/ical/5c9dc1a627cf55f1653d17573c2df58075d949559ec87e484b0cf90fa78bbf6d%40group.calendar.google.com/public/basic.ics"

ATTRIBUTION = (
    "Source: INRNG Pro Cycling Calendar – https://inrng.com/calendar/ "
    "Filtered calendar generated independently."
)

FILTERS = {
    "men-worldtour.ics": {
        "name": "Cycling – Men WorldTour",
        "description": "Men’s WorldTour races including one-day races and stage races.",
        "patterns": [r"\b1\.UWT\b", r"\b2\.UWT\b"],
    },

    "women-worldtour.ics": {
        "name": "Cycling – Women WorldTour",
        "description": "Women’s WorldTour races including one-day races and stage races.",
        "patterns": [r"\b1\.WWT\b", r"\b2\.WWT\b"],
    },

    #"worldtour-all.ics": {
    #    "name": "Cycling – WorldTour All",
    #    "description": "All WorldTour races, men and women combined.",
    #    "patterns": [r"\b1\.UWT\b", r"\b2\.UWT\b", r"\b1\.WWT\b", r"\b2\.WWT\b"],
    #},

    "pro-series-all.ics": {
        "name": "Cycling – ProSeries All",
        "description": "All ProSeries races including one-day races and stage races.",
        "patterns": [r"\b1\.Pro\b", r"\b2\.Pro\b"],
    },

    "class-1-all.ics": {
        "name": "Cycling – Class 1 All",
        "description": "All class 1 races including one-day races and stage races.",
        "patterns": [r"\b1\.1\b", r"\b2\.1\b"],
    },

    #"one-day-all.ics": {
    #    "name": "Cycling – One-Day Races All",
    #    "description": "All one-day races from the filtered calendar.",
    #    "patterns": [r"\b1\.(UWT|WWT|Pro|1)\b"],
    #},

    #"stage-races-all.ics": {
    #    "name": "Cycling – Stage Races All",
    #    "description": "All stage races from the filtered calendar.",
    #    "patterns": [r"\b2\.(UWT|WWT|Pro|1)\b"],
    #},
}