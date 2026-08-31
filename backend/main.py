from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import firebase_admin
from firebase_admin import credentials, firestore

from parser import parse_user_prompt


# ============================================================
# FIREBASE
# ============================================================

if not firebase_admin._apps:

    cred = credentials.Certificate(
        r"C:\sihproject\silentpearlsprotoai-firebase-key.json"
    )

    firebase_admin.initialize_app(cred)


db = firestore.client()


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="DesiTrails AI",
    description="AI Travel Recommendation System",
    version="9.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# REQUEST MODEL
# ============================================================

class UserPrompt(BaseModel):

    prompt: str


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "DesiTrails AI backend is running"
    }


# ============================================================
# TEXT CONVERTER
# ============================================================

def field_to_text(value):

    if value is None:
        return ""

    if isinstance(value, list):

        return " ".join(
            str(x)
            for x in value
        ).lower()

    return str(value).lower()


# ============================================================
# NUMBER CONVERTER
# ============================================================

def to_number(value, default=0):

    try:

        return float(value)

    except (
        ValueError,
        TypeError
    ):

        return default


# ============================================================
# TEXT MATCH
# ============================================================

def text_matches(
    destination,
    fields,
    keywords
):

    text = ""

    for field in fields:

        text += " " + field_to_text(
            destination.get(field)
        )

    text = text.lower()

    for keyword in keywords:

        if keyword.lower() in text:

            return True

    return False


# ============================================================
# ATTRIBUTE MATCH SCORE
# ============================================================

def get_attribute_score(
    destination,
    requirement
):

    # ========================================================
    # PEACEFUL
    # ========================================================

    if requirement == "peaceful":

        crowd = to_number(
            destination.get("crowd_score"),
            10
        )

        return max(
            0,
            min(
                100,
                (10 - crowd) / 10 * 100
            )
        )


    # ========================================================
    # CROWDED
    # ========================================================

    if requirement == "crowded":

        crowd = to_number(
            destination.get("crowd_score"),
            0
        )

        return max(
            0,
            min(
                100,
                crowd / 10 * 100
            )
        )


    # ========================================================
    # NATURE
    # ========================================================

    if requirement == "natural":

        score = to_number(
            destination.get("nature_score"),
            0
        )

        text_match = text_matches(
            destination,
            [
                "geography",
                "environment"
            ],
            [
                "natural",
                "nature",
                "green",
                "greenery",
                "forest",
                "mountain",
                "hill",
                "waterfall",
                "lake",
                "river",
                "beach",
                "coastal",
                "wildlife",
                "scenic",
                "landscape",
                "mangrove"
            ]
        )

        numeric_score = (
            score / 10
        ) * 100

        if text_match:
            return 100

        return min(
            100,
            numeric_score
        )


    # ========================================================
    # ADVENTURE
    # ========================================================

    if requirement == "adventure":

        score = to_number(
            destination.get("adventure_score"),
            0
        )

        return min(
            100,
            (score / 10) * 100
        )


    # ========================================================
    # CULTURE
    # ========================================================

    if requirement == "culture":

        score = to_number(
            destination.get("culture_score"),
            0
        )

        return min(
            100,
            (score / 10) * 100
        )


    # ========================================================
    # ACCESSIBILITY
    # ========================================================

    if requirement == "accessible":

        score = to_number(
            destination.get("accessibility_score"),
            0
        )

        return min(
            100,
            (score / 10) * 100
        )


    # ========================================================
    # REMOTE
    # ========================================================

    if requirement == "remote":

        score = to_number(
            destination.get("accessibility_score"),
            0
        )

        return max(
            0,
            min(
                100,
                100 - (score * 10)
            )
        )


    # ========================================================
    # TRADITIONAL
    # ========================================================

    if requirement == "traditional":

        return 100 if text_matches(
            destination,
            ["architecture"],
            [
                "traditional",
                "old style",
                "old-style",
                "old houses",
                "traditional houses",
                "heritage",
                "historic",
                "historical",
                "colonial"
            ]
        ) else 0


    # ========================================================
    # MODERN
    # ========================================================

    if requirement == "modern":

        return 100 if text_matches(
            destination,
            ["architecture"],
            [
                "modern",
                "contemporary"
            ]
        ) else 0


    # ========================================================
    # LESS MODERN
    # ========================================================

    if requirement == "less_modern":

        return 100 if text_matches(
            destination,
            [
                "architecture",
                "environment"
            ],
            [
                "traditional",
                "old",
                "heritage",
                "historic",
                "simple",
                "local",
                "rural",
                "village"
            ]
        ) else 0


    # ========================================================
    # SIMPLE
    # ========================================================

    if requirement == "simple":

        return 100 if text_matches(
            destination,
            [
                "architecture",
                "environment"
            ],
            [
                "simple",
                "basic",
                "local",
                "traditional",
                "rural",
                "village"
            ]
        ) else 0


    # ========================================================
    # RESIDENTIAL
    # ========================================================

    if requirement == "residential":

        return 100 if text_matches(
            destination,
            [
                "environment",
                "architecture"
            ],
            [
                "residential",
                "inhabited",
                "local",
                "village",
                "community",
                "residents",
                "settlement",
                "people live"
            ]
        ) else 0


    # ========================================================
    # FRIENDLY
    # ========================================================

    if requirement == "friendly":

        return 100 if text_matches(
            destination,
            ["environment"],
            [
                "friendly",
                "welcoming",
                "polite",
                "kind",
                "community"
            ]
        ) else 0


    # ========================================================
    # TEMPERATURE
    # ========================================================

    if requirement == "cold":

        return 100 if text_matches(
            destination,
            ["temperature"],
            [
                "cold",
                "cool",
                "chilly"
            ]
        ) else 0


    if requirement == "hot":

        return 100 if text_matches(
            destination,
            ["temperature"],
            [
                "hot",
                "warm"
            ]
        ) else 0


    if requirement == "comfortable":

        return 100 if text_matches(
            destination,
            ["temperature"],
            [
                "comfortable",
                "pleasant",
                "mild"
            ]
        ) else 0


    if requirement == "normal":

        return 100 if text_matches(
            destination,
            ["temperature"],
            [
                "normal",
                "moderate",
                "comfortable",
                "pleasant"
            ]
        ) else 0


    return 0


# ============================================================
# BUDGET NORMALIZATION
# ============================================================

def normalize_budget_scores(
    destinations,
    requirement
):

    budgets = [

        to_number(
            destination.get("budget"),
            0
        )

        for destination in destinations
    ]

    if not budgets:
        return {}

    minimum = min(budgets)
    maximum = max(budgets)

    scores = {}

    if maximum == minimum:

        for destination in destinations:

            name = str(
                destination.get(
                    "name",
                    ""
                )
            )

            scores[name] = 100

        return scores


    for destination in destinations:

        name = str(
            destination.get(
                "name",
                ""
            )
        )

        budget = to_number(
            destination.get("budget"),
            minimum
        )

        if requirement == "cheap":

            score = (
                (maximum - budget)
                /
                (maximum - minimum)
            ) * 100

        else:

            score = (
                (budget - minimum)
                /
                (maximum - minimum)
            ) * 100

        scores[name] = max(
            0,
            min(
                100,
                score
            )
        )

    return scores


# ============================================================
# FINAL MATCH SCORE
# ============================================================

def calculate_match_score(
    destination,
    requirements,
    budget_scores
):

    if not requirements:

        return 0


    scores = []


    for requirement in requirements:

        if requirement in [
            "cheap",
            "expensive"
        ]:

            name = str(
                destination.get(
                    "name",
                    ""
                )
            )

            score = budget_scores.get(
                name,
                0
            )

        else:

            score = get_attribute_score(
                destination,
                requirement
            )


        scores.append(
            max(
                0,
                min(
                    100,
                    score
                )
            )
        )


    if not scores:
        return 0


    final_score = sum(scores) / len(scores)


    return round(
        max(
            0,
            min(
                100,
                final_score
            )
        ),
        2
    )


# ============================================================
# DESTINATION DESCRIPTION
# ============================================================

def create_description(destination):

    environment = str(
        destination.get(
            "environment",
            ""
        )
    ).strip()

    geography = str(
        destination.get(
            "geography",
            ""
        )
    ).strip()

    if environment:
        return environment.capitalize() + "."

    if geography:
        return geography.capitalize() + "."

    return (
        "A beautiful lesser-known destination "
        "waiting to be explored."
    )


# ============================================================
# BUILD RECOMMENDATION
# ============================================================

def build_recommendation(
    destination,
    score
):

    return {

        "name":
            destination.get("name"),

        "state":
            destination.get("state"),

        "latitude":
            destination.get("latitude"),

        "longitude":
            destination.get("longitude"),

        "budget":
            destination.get("budget"),

        "nature_score":
            destination.get("nature_score"),

        "adventure_score":
            destination.get("adventure_score"),

        "culture_score":
            destination.get("culture_score"),

        "crowd_score":
            destination.get("crowd_score"),

        "accessibility_score":
            destination.get("accessibility_score"),

        "best_season":
            destination.get("best_season"),

        "tourism_saturation":
            destination.get("tourism_saturation"),

        "geography":
            destination.get(
                "geography",
                ""
            ),

        "architecture":
            destination.get(
                "architecture",
                ""
            ),

        "environment":
            destination.get(
                "environment",
                ""
            ),

        "temperature":
            destination.get(
                "temperature",
                ""
            ),

        "description":
            create_description(
                destination
            ),

        "match_score":
            score
    }


# ============================================================
# GET ALL DESTINATIONS
# ============================================================

@app.get("/destinations")
def get_destinations():

    docs = db.collection(
        "destinations"
    ).stream()

    destinations = []

    seen_locations = set()


    for doc in docs:

        data = doc.to_dict()

        name = str(
            data.get(
                "name",
                ""
            )
        ).strip().lower()


        if not name:
            continue


        if name in seen_locations:
            continue


        seen_locations.add(name)

        destinations.append(data)


    return {
        "destinations": destinations
    }


# ============================================================
# RECOMMEND FROM USER PROMPT
# ============================================================

@app.post("/recommend-from-prompt")
def recommend_from_prompt(
    user_prompt: UserPrompt
):

    # ========================================================
    # PARSE PROMPT
    # ========================================================

    parsed = parse_user_prompt(
        user_prompt.prompt
    )


    # ========================================================
    # NON-TRAVEL
    # ========================================================

    if not parsed.get(
        "travel_related",
        False
    ):

        return {

            "success": False,

            "message":
                "Ask relevant questions related to travel",

            "recommendations": []
        }


    # ========================================================
    # FOREIGN LOCATION
    # ========================================================

    if parsed.get(
        "invalid_location",
        False
    ):

        return {

            "success": False,

            "message":
                "Please give only the names of Indian states.",

            "recommendations": []
        }


    # ========================================================
    # STATES
    # ========================================================

    requested_states = parsed.get(
        "states",
        []
    )


    requested_states_lower = [
        state.lower()
        for state in requested_states
    ]


    # ========================================================
    # REQUIREMENTS
    # ========================================================

    requirements = parsed.get(
        "requirements",
        []
    )


    # ========================================================
    # GET FIRESTORE DATA
    # ========================================================

    docs = db.collection(
        "destinations"
    ).stream()


    destinations = []

    seen_locations = set()


    for doc in docs:

        destination = doc.to_dict()


        name = str(
            destination.get(
                "name",
                ""
            )
        ).strip()


        if not name:
            continue


        name_key = name.lower()


        if name_key in seen_locations:
            continue


        seen_locations.add(
            name_key
        )


        # ----------------------------------------------------
        # STATE FILTER
        # ----------------------------------------------------

        if requested_states_lower:

            destination_state = str(
                destination.get(
                    "state",
                    ""
                )
            ).strip().lower()


            if destination_state not in requested_states_lower:
                continue


        destinations.append(
            destination
        )


    # ========================================================
    # NO DESTINATIONS
    # ========================================================

    if not destinations:

        return {

            "success": False,

            "message":
                "No destinations found for the selected state.",

            "recommendations": []
        }


    # ========================================================
    # BUDGET SCORES
    # ========================================================

    budget_requirement = None


    if "cheap" in requirements:

        budget_requirement = "cheap"

    elif "expensive" in requirements:

        budget_requirement = "expensive"


    if budget_requirement:

        budget_scores = normalize_budget_scores(
            destinations,
            budget_requirement
        )

    else:

        budget_scores = {}


    # ========================================================
    # CALCULATE SCORES
    # ========================================================

    scored_destinations = []


    for destination in destinations:

        score = calculate_match_score(
            destination,
            requirements,
            budget_scores
        )


        scored_destinations.append(
            (
                destination,
                score
            )
        )


    # ========================================================
    # SORT BY MATCH SCORE
    # ========================================================

    scored_destinations.sort(
        key=lambda x: x[1],
        reverse=True
    )


    # ========================================================
    # LIMIT RESULTS
    #
    # Maximum 3 recommendations.
    # ========================================================

    top_destinations = (
        scored_destinations[:3]
    )


    # ========================================================
    # BUILD RESPONSE
    # ========================================================

    recommendations = []


    for destination, score in top_destinations:

        recommendations.append(
            build_recommendation(
                destination,
                score
            )
        )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "success": True,

        "message":
            "Recommendations generated successfully",

        "parsed_preferences": parsed,

        "recommendations":
            recommendations
    }