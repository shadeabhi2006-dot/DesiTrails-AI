import re


# ============================================================
# DESITRAILS AI - NATURAL LANGUAGE PARSER
# Designed for the current destinations.csv structure
# ============================================================

INDIAN_LOCATIONS = {
    "andhra pradesh", "arunachal pradesh", "assam", "bihar",
    "chhattisgarh", "goa", "gujarat", "haryana", "himachal pradesh",
    "jharkhand", "karnataka", "kerala", "madhya pradesh", "maharashtra",
    "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab",
    "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura",
    "uttar pradesh", "uttarakhand", "west bengal",
    # Included because it is present in the DesiTrails dataset.
    "jammu and kashmir",
}

STATE_ALIASES = {
    "bengal": "west bengal",
    "wb": "west bengal",
    "up": "uttar pradesh",
    "uk": "uttarakhand",
    "hp": "himachal pradesh",
    "mp": "madhya pradesh",
    "ap": "andhra pradesh",
    "tn": "tamil nadu",
    "orissa": "odisha",
    "j&k": "jammu and kashmir",
    "j and k": "jammu and kashmir",
    "jammu & kashmir": "jammu and kashmir",
    "kashmir": "jammu and kashmir",
}

FOREIGN_LOCATIONS = {
    "usa", "united states", "america", "canada", "mexico", "brazil",
    "argentina", "united kingdom", "england", "scotland", "wales",
    "london", "france", "germany", "italy", "spain", "portugal",
    "switzerland", "austria", "nepal", "bhutan", "bangladesh",
    "pakistan", "sri lanka", "myanmar", "japan", "china", "south korea",
    "korea", "thailand", "singapore", "malaysia", "indonesia",
    "vietnam", "philippines", "australia", "new zealand", "dubai",
    "uae", "united arab emirates", "saudi arabia", "qatar", "russia",
    "ukraine", "turkey", "egypt", "south africa",
}

TRAVEL_KEYWORDS = {
    "travel", "travelling", "traveling", "trip", "tour", "tourism",
    "tourist", "destination", "destinations", "visit", "visiting",
    "vacation", "holiday", "getaway", "journey", "place", "places",
    "location", "locations", "city", "cities", "state", "states",
    "nature", "natural", "beach", "beaches", "mountain", "mountains",
    "valley", "valleys", "forest", "waterfall", "waterfalls", "lake",
    "river", "cave", "meadow", "backwaters", "ghat", "adventure",
    "trek", "trekking", "hiking", "camping", "heritage", "historical",
    "history", "culture", "cultural", "architecture", "budget", "cheap",
    "cheapest", "affordable", "expensive", "luxury", "peaceful", "peace",
    "calm", "quiet", "crowded", "crowdy", "weather", "temperature",
    "houses", "house", "modern", "traditional", "people", "residents",
    "community", "friendly", "polite", "simple", "season",
}

GROUPS = {
    "cheap": [
        "cheap", "cheapest", "affordable", "low budget", "inexpensive",
        "economical", "budget friendly", "budget-friendly", "backpacking",
        "backpacker",
    ],
    "expensive": [
        "expensive", "luxury", "premium", "lavish", "high budget", "fancy",
    ],
    "peaceful": [
        "peaceful", "peace", "calm", "quiet", "serene", "relaxed",
        "relaxing", "less crowded", "not crowded", "uncrowded",
        "tranquil", "not busy", "low crowd", "low crowds",
    ],
    "crowded": [
        "crowded", "crowdy", "busy", "popular", "heavily crowded",
    ],
    "natural": [
        "nature", "natural", "natural beauty", "green", "greenery",
        "forest", "forests", "mountain", "mountains", "hill", "hills",
        "waterfall", "waterfalls", "lake", "river", "beach", "beaches",
        "coastal", "coast", "wildlife", "scenic", "landscape", "mangrove",
    ],
    "adventure": [
        "adventure", "adventurous", "trek", "trekking", "hiking", "camping",
        "rafting", "climbing", "explore", "exploration",
    ],
    "culture": [
        "culture", "cultural", "heritage", "historical", "history", "temple",
        "temples", "monument", "monuments", "museum", "colonial",
    ],
    "accessible": [
        "accessible", "easy to reach", "easy access", "well connected",
        "easy transportation", "easy transport", "good connectivity",
    ],
    "remote": [
        "remote", "isolated", "hard to reach", "difficult to reach", "offbeat",
    ],
    "traditional": [
        "traditional", "old style", "old-style", "old houses",
        "traditional houses", "heritage houses", "heritage home",
        "heritage homes", "old buildings", "historic buildings", "colonial",
    ],
    "modern": [
        "modern", "modern houses", "modern house", "modern homes",
        "modern home", "contemporary",
    ],
    "less_modern": [
        "not heavily modern", "not too modern", "not very modern",
        "less modern",
    ],
    "simple": [
        "not fancy", "simple", "not luxurious", "not luxury", "simple houses",
        "simple homes",
    ],
    "residential": [
        "people live there", "people live", "lived in", "residential",
        "residents", "local people", "local community", "living community",
        "inhabited", "not abandoned",
    ],
    "friendly": [
        "friendly", "polite", "welcoming", "good people", "friendly people",
        "polite people", "welcoming people", "kind people",
    ],
}

TEMPERATURE_GROUPS = {
    "cold": ["cold", "cool", "chilly", "cold weather", "cool weather"],
    "hot": ["hot", "hot weather", "very warm", "very hot", "heat"],
    "comfortable": [
        "comfortable weather", "comfortable temperature",
        "pleasant weather", "pleasant temperature", "mild weather",
        "mild temperature",
    ],
    "normal": [
        "normal temperature", "normal weather", "moderate temperature",
        "moderate weather",
    ],
}

SEASON_WORDS = {
    "winter": ["winter", "winters"],
    "summer": ["summer", "summers"],
    "monsoon": ["monsoon", "rainy season", "rain"],
    "spring": ["spring"],
    "autumn": ["autumn", "fall"],
}

GEOGRAPHY_GROUPS = {
    "beach": ["beach", "beaches", "coast", "coastal", "seaside"],
    "mountain": ["mountain", "mountains", "hill", "hills", "himalayan"],
    "forest": ["forest", "forests", "jungle", "wooded"],
    "waterfall": ["waterfall", "waterfalls", "cascade", "cascading"],
    "lake": ["lake", "lakes", "backwater", "backwaters"],
    "river": ["river", "rivers", "riverbank", "riverside"],
    "valley": ["valley", "valleys"],
    "cave": ["cave", "caves"],
}


def _contains(text, phrases):
    text = text.lower()
    for phrase in phrases:
        phrase = phrase.lower()
        if re.search(r"\b" + re.escape(phrase) + r"\b", text):
            return True
    return False


def extract_states(text):
    t = text.lower()
    found = []

    # Longest first prevents partial/ambiguous matches.
    candidates = sorted(INDIAN_LOCATIONS, key=len, reverse=True)

    for state in candidates:
        if re.search(r"\b" + re.escape(state) + r"\b", t):
            if state not in found:
                found.append(state)

    for alias, state in STATE_ALIASES.items():
        if re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", t):
            if state not in found:
                found.append(state)

    return [x.title() for x in found]


def contains_foreign_location(text):
    t = text.lower()
    return any(
        re.search(r"\b" + re.escape(location) + r"\b", t)
        for location in FOREIGN_LOCATIONS
    )


def extract_temperature(text):
    for requirement, words in TEMPERATURE_GROUPS.items():
        if _contains(text, words):
            return requirement
    return None


def extract_seasons(text):
    seasons = []
    for season, words in SEASON_WORDS.items():
        if _contains(text, words):
            seasons.append(season)
    return seasons


def extract_geography(text):
    found = []
    for category, words in GEOGRAPHY_GROUPS.items():
        if _contains(text, words):
            found.append(category)
    return found


def parse_user_prompt(text):
    text = (text or "").strip()

    if not text:
        return {
            "travel_related": False,
            "invalid_location": False,
            "states": [],
            "requirements": [],
            "temperature": None,
            "seasons": [],
            "geography": [],
            "message": "Ask relevant questions related to travel",
        }

    if contains_foreign_location(text):
        return {
            "travel_related": True,
            "invalid_location": True,
            "states": [],
            "requirements": [],
            "temperature": None,
            "seasons": [],
            "geography": [],
            "message": "Please give only the names of Indian states.",
        }

    states = extract_states(text)
    temperature = extract_temperature(text)
    seasons = extract_seasons(text)
    geography = extract_geography(text)

    requirements = []

    # Order matters for phrases such as "less crowded".
    checks = [
        ("cheap", GROUPS["cheap"]),
        ("expensive", GROUPS["expensive"]),
        ("peaceful", GROUPS["peaceful"]),
        ("crowded", GROUPS["crowded"]),
        ("natural", GROUPS["natural"]),
        ("adventure", GROUPS["adventure"]),
        ("culture", GROUPS["culture"]),
        ("accessible", GROUPS["accessible"]),
        ("remote", GROUPS["remote"]),
        ("less_modern", GROUPS["less_modern"]),
        ("modern", GROUPS["modern"]),
        ("traditional", GROUPS["traditional"]),
        ("simple", GROUPS["simple"]),
        ("residential", GROUPS["residential"]),
        ("friendly", GROUPS["friendly"]),
    ]

    for requirement, words in checks:
        if _contains(text, words):
            requirements.append(requirement)

    if temperature:
        requirements.append(temperature)

    # A geography word is already a strong travel signal, but we keep it
    # separately so the backend can use the descriptive CSV fields.
    if not any(requirement == "natural" for requirement in requirements):
        natural_geo = {"beach", "mountain", "forest", "waterfall", "lake",
                       "river", "valley", "cave"}
        if natural_geo.intersection(geography):
            requirements.append("natural")

    requirements = list(dict.fromkeys(requirements))

    travel_words_present = _contains(text, TRAVEL_KEYWORDS)
    travel_related = bool(
        travel_words_present or states or requirements or temperature or seasons
        or geography
    )

    if not travel_related:
        return {
            "travel_related": False,
            "invalid_location": False,
            "states": [],
            "requirements": [],
            "temperature": None,
            "seasons": [],
            "geography": [],
            "message": "Ask relevant questions related to travel",
        }

    return {
        "travel_related": True,
        "invalid_location": False,
        "states": states,
        "requirements": requirements,
        "temperature": temperature,
        "seasons": seasons,
        "geography": geography,
        "message": "Travel preferences extracted successfully",
    }
