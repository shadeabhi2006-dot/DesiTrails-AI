import re


# ============================================================
# INDIAN STATES
# ============================================================

INDIAN_STATES = [
    "andhra pradesh",
    "arunachal pradesh",
    "assam",
    "bihar",
    "chhattisgarh",
    "goa",
    "gujarat",
    "haryana",
    "himachal pradesh",
    "jharkhand",
    "karnataka",
    "kerala",
    "madhya pradesh",
    "maharashtra",
    "manipur",
    "meghalaya",
    "mizoram",
    "nagaland",
    "odisha",
    "punjab",
    "rajasthan",
    "sikkim",
    "tamil nadu",
    "telangana",
    "tripura",
    "uttar pradesh",
    "uttarakhand",
    "west bengal"
]


# ============================================================
# STATE ALIASES
# ============================================================

STATE_ALIASES = {

    "bengal":
        "west bengal",

    "wb":
        "west bengal",

    "up":
        "uttar pradesh",

    "uk":
        "uttarakhand",

    "hp":
        "himachal pradesh",

    "mp":
        "madhya pradesh",

    "ap":
        "andhra pradesh",

    "tn":
        "tamil nadu",

    "orissa":
        "odisha"
}


# ============================================================
# FOREIGN LOCATIONS
# ============================================================

FOREIGN_LOCATIONS = [

    "usa",
    "united states",
    "america",
    "canada",
    "mexico",
    "brazil",
    "argentina",

    "united kingdom",
    "england",
    "scotland",
    "wales",
    "london",

    "france",
    "germany",
    "italy",
    "spain",
    "portugal",
    "switzerland",
    "austria",

    "nepal",
    "bhutan",
    "bangladesh",
    "pakistan",
    "sri lanka",
    "myanmar",

    "japan",
    "china",
    "south korea",
    "korea",

    "thailand",
    "singapore",
    "malaysia",
    "indonesia",
    "vietnam",
    "philippines",

    "australia",
    "new zealand",

    "dubai",
    "uae",
    "united arab emirates",

    "saudi arabia",
    "qatar",

    "russia",
    "ukraine",
    "turkey",
    "egypt",
    "south africa"
]


# ============================================================
# TRAVEL KEYWORDS
# ============================================================

TRAVEL_KEYWORDS = [

    "travel",
    "travelling",
    "traveling",
    "trip",
    "tour",
    "tourism",
    "tourist",

    "destination",
    "destinations",

    "visit",
    "visiting",

    "vacation",
    "holiday",
    "getaway",
    "journey",

    "place",
    "places",

    "location",
    "locations",

    "city",
    "cities",

    "state",
    "states",

    "nature",
    "natural",

    "beach",
    "mountain",
    "mountains",
    "forest",
    "waterfall",
    "lake",
    "river",

    "adventure",
    "trek",
    "trekking",
    "hiking",
    "camping",

    "heritage",
    "historical",
    "history",
    "culture",
    "cultural",
    "architecture",

    "budget",
    "cheap",
    "cheapest",
    "affordable",
    "expensive",

    "luxury",
    "peaceful",
    "peace",
    "calm",
    "quiet",

    "crowded",
    "crowdy",
    "less crowded",

    "weather",
    "temperature",

    "houses",
    "house",

    "modern",
    "traditional",

    "people",
    "residents",
    "community",

    "friendly",
    "polite",
    "simple"
]


# ============================================================
# ATTRIBUTE WORDS
# ============================================================

NATURE_WORDS = [
    "nature",
    "natural",
    "natural beauty",
    "green",
    "greenery",
    "forest",
    "forests",
    "mountain",
    "mountains",
    "hill",
    "hills",
    "waterfall",
    "lake",
    "river",
    "beach",
    "coastal",
    "coast",
    "wildlife",
    "scenic",
    "landscape",
    "mangrove"
]


ADVENTURE_WORDS = [
    "adventure",
    "adventurous",
    "trek",
    "trekking",
    "hiking",
    "camping",
    "rafting",
    "climbing",
    "explore",
    "exploration"
]


CULTURE_WORDS = [
    "culture",
    "cultural",
    "heritage",
    "historical",
    "history",
    "temple",
    "temples",
    "monument",
    "monuments",
    "museum",
    "colonial"
]


CHEAP_WORDS = [
    "cheap",
    "cheapest",
    "affordable",
    "low budget",
    "inexpensive",
    "economical",
    "budget friendly",
    "budget-friendly",
    "backpacking",
    "backpacker"
]


EXPENSIVE_WORDS = [
    "expensive",
    "luxury",
    "premium",
    "lavish",
    "high budget",
    "fancy"
]


PEACEFUL_WORDS = [
    "peaceful",
    "peace",
    "calm",
    "quiet",
    "serene",
    "relaxed",
    "relaxing",
    "less crowded",
    "not crowded",
    "uncrowded",
    "mind fresh",
    "refreshing",
    "tranquil",
    "not busy"
]


CROWDED_WORDS = [
    "crowded",
    "crowdy",
    "busy",
    "popular",
    "heavily crowded"
]


ACCESSIBLE_WORDS = [
    "accessible",
    "easy to reach",
    "easy access",
    "well connected",
    "easy transportation",
    "easy transport"
]


REMOTE_WORDS = [
    "remote",
    "isolated",
    "hard to reach",
    "difficult to reach",
    "offbeat"
]


TRADITIONAL_WORDS = [
    "traditional",
    "old style",
    "old-style",
    "old houses",
    "traditional houses",
    "heritage houses",
    "heritage home",
    "heritage homes",
    "old buildings",
    "historic buildings",
    "colonial"
]


MODERN_WORDS = [
    "modern",
    "modern houses",
    "modern house",
    "modern homes",
    "modern home",
    "contemporary"
]


LESS_MODERN_WORDS = [
    "not heavily modern",
    "not too modern",
    "not very modern",
    "less modern"
]


SIMPLE_WORDS = [
    "not fancy",
    "simple",
    "not luxurious",
    "not luxury",
    "simple houses",
    "simple homes"
]


RESIDENTIAL_WORDS = [
    "people live there",
    "people live",
    "lived in",
    "residential",
    "residents",
    "local people",
    "local community",
    "living community",
    "inhabited",
    "not abandoned"
]


FRIENDLY_WORDS = [
    "friendly",
    "polite",
    "welcoming",
    "good people",
    "friendly people",
    "polite people",
    "welcoming people",
    "kind people"
]


COLD_WORDS = [
    "cold",
    "cool",
    "chilly",
    "cold weather",
    "cool weather"
]


HOT_WORDS = [
    "hot",
    "hot weather",
    "very warm",
    "very hot",
    "heat"
]


COMFORTABLE_WORDS = [
    "comfortable weather",
    "comfortable temperature",
    "pleasant weather",
    "pleasant temperature",
    "mild weather",
    "mild temperature"
]


NORMAL_WORDS = [
    "normal temperature",
    "normal weather",
    "moderate temperature",
    "moderate weather"
]


# ============================================================
# KEYWORD FUNCTION
# ============================================================

def contains_keyword(text, keywords):

    text = text.lower()

    for keyword in keywords:

        keyword = keyword.lower()

        if " " in keyword:

            if keyword in text:
                return True

        else:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(
                pattern,
                text
            ):
                return True

    return False


# ============================================================
# EXTRACT STATES
# ============================================================

def extract_states(text):

    text_lower = text.lower()

    found_states = []


    for state in sorted(
        INDIAN_STATES,
        key=len,
        reverse=True
    ):

        pattern = (
            r"\b" +
            re.escape(state) +
            r"\b"
        )

        if re.search(
            pattern,
            text_lower
        ):

            if state not in found_states:

                found_states.append(
                    state
                )


    for alias, state in STATE_ALIASES.items():

        pattern = (
            r"\b" +
            re.escape(alias) +
            r"\b"
        )

        if re.search(
            pattern,
            text_lower
        ):

            if state not in found_states:

                found_states.append(
                    state
                )


    return [
        state.title()
        for state in found_states
    ]


# ============================================================
# FOREIGN LOCATION
# ============================================================

def contains_foreign_location(text):

    text_lower = text.lower()


    for location in FOREIGN_LOCATIONS:

        pattern = (
            r"\b" +
            re.escape(location) +
            r"\b"
        )

        if re.search(
            pattern,
            text_lower
        ):

            return True


    return False


# ============================================================
# TEMPERATURE
# ============================================================

def extract_temperature(text):

    if contains_keyword(
        text,
        COLD_WORDS
    ):
        return "cold"


    if contains_keyword(
        text,
        HOT_WORDS
    ):
        return "hot"


    if contains_keyword(
        text,
        COMFORTABLE_WORDS
    ):
        return "comfortable"


    if contains_keyword(
        text,
        NORMAL_WORDS
    ):
        return "normal"


    return None


# ============================================================
# PARSER
# ============================================================

def parse_user_prompt(text):

    if not text or not text.strip():

        return {

            "travel_related": False,

            "invalid_location": False,

            "message":
                "Ask relevant questions related to travel"
        }


    # ========================================================
    # FOREIGN LOCATION
    # ========================================================

    if contains_foreign_location(text):

        return {

            "travel_related": True,

            "invalid_location": True,

            "message":
                "Please give only the names of Indian states."
        }


    # ========================================================
    # TRAVEL CHECK
    # ========================================================

    if not contains_keyword(
        text,
        TRAVEL_KEYWORDS
    ):

        return {

            "travel_related": False,

            "invalid_location": False,

            "message":
                "Ask relevant questions related to travel"
        }


    requirements = []


    # ========================================================
    # BUDGET
    # ========================================================

    if contains_keyword(
        text,
        CHEAP_WORDS
    ):

        requirements.append(
            "cheap"
        )

    elif contains_keyword(
        text,
        EXPENSIVE_WORDS
    ):

        requirements.append(
            "expensive"
        )


    # ========================================================
    # NATURE
    # ========================================================

    if contains_keyword(
        text,
        NATURE_WORDS
    ):

        requirements.append(
            "natural"
        )


    # ========================================================
    # ADVENTURE
    # ========================================================

    if contains_keyword(
        text,
        ADVENTURE_WORDS
    ):

        requirements.append(
            "adventure"
        )


    # ========================================================
    # CULTURE
    # ========================================================

    if contains_keyword(
        text,
        CULTURE_WORDS
    ):

        requirements.append(
            "culture"
        )


    # ========================================================
    # CROWD
    # ========================================================

    if contains_keyword(
        text,
        PEACEFUL_WORDS
    ):

        requirements.append(
            "peaceful"
        )

    elif contains_keyword(
        text,
        CROWDED_WORDS
    ):

        requirements.append(
            "crowded"
        )


    # ========================================================
    # ACCESSIBILITY
    # ========================================================

    if contains_keyword(
        text,
        ACCESSIBLE_WORDS
    ):

        requirements.append(
            "accessible"
        )

    elif contains_keyword(
        text,
        REMOTE_WORDS
    ):

        requirements.append(
            "remote"
        )


    # ========================================================
    # ARCHITECTURE
    # ========================================================

    # Check less-modern FIRST so that
    # "less modern" doesn't become "modern".

    if contains_keyword(
        text,
        LESS_MODERN_WORDS
    ):

        requirements.append(
            "less_modern"
        )

    elif contains_keyword(
        text,
        MODERN_WORDS
    ):

        requirements.append(
            "modern"
        )


    if contains_keyword(
        text,
        TRADITIONAL_WORDS
    ):

        requirements.append(
            "traditional"
        )


    if contains_keyword(
        text,
        SIMPLE_WORDS
    ):

        requirements.append(
            "simple"
        )


    # ========================================================
    # ENVIRONMENT
    # ========================================================

    if contains_keyword(
        text,
        RESIDENTIAL_WORDS
    ):

        requirements.append(
            "residential"
        )


    if contains_keyword(
        text,
        FRIENDLY_WORDS
    ):

        requirements.append(
            "friendly"
        )


    # ========================================================
    # TEMPERATURE
    # ========================================================

    temperature = extract_temperature(
        text
    )


    if temperature:

        requirements.append(
            temperature
        )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    requirements = list(
        dict.fromkeys(
            requirements
        )
    )


    # ========================================================
    # FINAL PARSED RESULT
    # ========================================================

    return {

        "travel_related": True,

        "invalid_location": False,

        "states":
            extract_states(text),

        "requirements":
            requirements,

        "temperature":
            temperature,

        "message":
            "Travel preferences extracted successfully"
    }