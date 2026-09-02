from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import firebase_admin
from firebase_admin import credentials, firestore

import os
import json
import re

from parser import parse_user_prompt


# ============================================================
# FIREBASE
# ============================================================

if not firebase_admin._apps:
    firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")

    if not firebase_credentials:
        raise RuntimeError("FIREBASE_CREDENTIALS environment variable is not set")

    cred = credentials.Certificate(json.loads(firebase_credentials))
    firebase_admin.initialize_app(cred)

db = firestore.client()


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="DesiTrails AI",
    description="AI Travel Recommendation System",
    version="10.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class UserPrompt(BaseModel):
    prompt: str


# ============================================================
# HELPERS
# ============================================================

def to_number(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


def text(value):
    return str(value or "").strip().lower()


def destination_text(destination, fields):
    return " ".join(text(destination.get(field)) for field in fields)


def contains_any(value, words):
    value = text(value)
    return any(
        re.search(r"(?<!\w)" + re.escape(word.lower()) + r"(?!\w)", value)
        for word in words
    )


def clamp(value):
    return round(max(0.0, min(100.0, float(value))), 2)


# ============================================================
# ATTRIBUTE SCORING
# The score is based only on attributes actually detected
# in the user's prompt.
# ============================================================

def attribute_score(destination, requirement, geography_terms):
    if requirement == "peaceful":
        # Lower crowd_score means more peaceful.
        crowd = to_number(destination.get("crowd_score"), 5)
        score = (10 - crowd) * 10

        env = destination_text(destination, ["environment"])
        saturation = text(destination.get("tourism_saturation"))

        if any(word in env for word in ["peaceful", "quiet", "serene",
                                        "tranquil", "low-density", "uncrowded",
                                        "secluded"]):
            score += 10

        if saturation in {"very low", "low"}:
            score += 5

        return clamp(score)

    if requirement == "crowded":
        crowd = to_number(destination.get("crowd_score"), 5)
        return clamp(crowd * 10)

    if requirement == "natural":
        numeric = to_number(destination.get("nature_score"), 0) * 10
        geo = destination_text(destination, ["geography", "environment"])

        nature_words = {
            "nature", "natural", "green", "greenery", "forest", "forests",
            "mountain", "mountains", "hill", "hills", "waterfall",
            "waterfalls", "lake", "river", "beach", "coastal", "wildlife",
            "scenic", "landscape", "mangrove", "valley", "meadow", "misty",
        }

        matches = sum(1 for word in nature_words if word in geo)
        text_bonus = min(15, matches * 3)

        # Numerical nature score is the main signal; descriptions refine it.
        return clamp(numeric * 0.85 + text_bonus)

    if requirement == "adventure":
        numeric = to_number(destination.get("adventure_score"), 0) * 10
        geo = destination_text(destination, ["geography", "environment"])

        adventure_words = {
            "rugged", "rocky", "mountain", "hills", "cave", "waterfall",
            "trek", "streams", "gorge", "cliffs", "remote", "adventure",
        }
        bonus = min(15, sum(1 for word in adventure_words if word in geo) * 3)
        return clamp(numeric * 0.85 + bonus)

    if requirement == "culture":
        numeric = to_number(destination.get("culture_score"), 0) * 10
        descriptive = destination_text(destination, ["architecture", "environment"])

        culture_words = {
            "traditional", "heritage", "historic", "historical", "temple",
            "colonial", "cultural", "village", "tribal", "traditional",
            "craftsmanship", "megalithic", "spiritual",
        }
        bonus = min(15, sum(1 for word in culture_words if word in descriptive) * 3)
        return clamp(numeric * 0.85 + bonus)

    if requirement == "accessible":
        return clamp(to_number(destination.get("accessibility_score"), 0) * 10)

    if requirement == "remote":
        accessibility = to_number(destination.get("accessibility_score"), 5)
        saturation = text(destination.get("tourism_saturation"))

        score = (10 - accessibility) * 10
        if saturation == "very low":
            score += 15
        elif saturation == "low":
            score += 10

        env = destination_text(destination, ["environment", "geography"])
        if any(word in env for word in ["remote", "secluded", "pristine", "untouched"]):
            score += 10

        return clamp(score)

    if requirement == "traditional":
        value = destination_text(destination, ["architecture", "environment"])
        words = [
            "traditional", "heritage", "historic", "colonial", "rural",
            "village", "tribal", "local",
        ]
        return 100 if any(word in value for word in words) else 20

    if requirement == "modern":
        value = destination_text(destination, ["architecture", "environment"])
        return 100 if any(word in value for word in ["modern", "contemporary"]) else 20

    if requirement == "less_modern":
        value = destination_text(destination, ["architecture", "environment"])
        words = ["traditional", "old", "heritage", "historic", "simple", "local", "rural"]
        return 100 if any(word in value for word in words) else 20

    if requirement == "simple":
        value = destination_text(destination, ["architecture", "environment"])
        words = ["simple", "basic", "local", "traditional", "rural", "village", "rustic"]
        return 100 if any(word in value for word in words) else 20

    if requirement == "residential":
        value = destination_text(destination, ["architecture", "environment"])
        words = ["village", "local", "community", "residents", "settlement", "homes", "houses"]
        return 100 if any(word in value for word in words) else 20

    if requirement == "friendly":
        value = destination_text(destination, ["environment"])
        words = ["welcoming", "friendly", "community", "local"]
        return 100 if any(word in value for word in words) else 20

    if requirement == "cold":
        value = text(destination.get("temperature"))
        return 100 if any(word in value for word in ["cold", "cool", "chilly"]) else 20

    if requirement == "hot":
        value = text(destination.get("temperature"))
        return 100 if any(word in value for word in ["hot", "warm"]) else 20

    if requirement == "comfortable":
        value = text(destination.get("temperature"))
        return 100 if any(word in value for word in ["comfortable", "pleasant", "mild"]) else 20

    if requirement == "normal":
        value = text(destination.get("temperature"))
        return 100 if any(word in value for word in ["normal", "moderate", "comfortable", "pleasant"]) else 20

    return 0


# ============================================================
# BUDGET SCORING
# Lower budget = better "cheap" match.
# Higher budget = better "expensive" match.
#
# The calculation is done AFTER state filtering, so:
# "cheap place in Jammu and Kashmir"
# compares the J&K destinations with one another.
# ============================================================

def budget_scores(destinations, requirement):
    if not destinations:
        return {}

    values = [to_number(d.get("budget"), 0) for d in destinations]
    minimum = min(values)
    maximum = max(values)

    result = {}

    if minimum == maximum:
        return {
            text(d.get("name")): 100.0
            for d in destinations
        }

    for destination in destinations:
        name = text(destination.get("name"))
        budget = to_number(destination.get("budget"), minimum)

        if requirement == "cheap":
            score = ((maximum - budget) / (maximum - minimum)) * 100
        else:
            score = ((budget - minimum) / (maximum - minimum)) * 100

        result[name] = clamp(score)

    return result


# ============================================================
# SEASON SCORING
# ============================================================

def season_score(destination, requested_seasons):
    if not requested_seasons:
        return None

    value = text(destination.get("best_season"))
    if not value:
        return 0

    score = 0
    for season in requested_seasons:
        if season in value:
            score = max(score, 100)

        # Spring & Autumn etc.
        if season == "spring" and "spring" in value:
            score = 100
        if season == "autumn" and ("autumn" in value or "fall" in value):
            score = 100

    return score


# ============================================================
# GEOGRAPHY SCORING
# ============================================================

def geography_score(destination, requested_geography):
    if not requested_geography:
        return None

    value = destination_text(destination, ["geography", "environment"])

    mapping = {
        "beach": ["beach", "coast", "coastal", "seaside"],
        "mountain": ["mountain", "hills", "himalayan", "highland", "plateau"],
        "forest": ["forest", "forested", "jungle", "wooded"],
        "waterfall": ["waterfall", "waterfalls", "cascading", "cascade"],
        "lake": ["lake", "backwater", "backwaters", "reservoir"],
        "river": ["river", "riverbank", "riverside", "stream", "streams"],
        "valley": ["valley", "valleys", "gorge"],
        "cave": ["cave", "caves"],
    }

    matched = 0
    total = len(requested_geography)

    for category in requested_geography:
        words = mapping.get(category, [category])
        if any(word in value for word in words):
            matched += 1

    return clamp((matched / total) * 100)


# ============================================================
# FINAL MATCH SCORE
# ============================================================

def calculate_match_score(destination, requirements, requested_seasons, requested_geography):
    scores = []

    budget_req = None
    if "cheap" in requirements:
        budget_req = "cheap"
    elif "expensive" in requirements:
        budget_req = "expensive"

    # Budget scores are injected separately.
    return scores, budget_req


def score_destination(destination, requirements, requested_seasons,
                       requested_geography, budget_map):
    scores = []

    for requirement in requirements:
        if requirement in {"cheap", "expensive"}:
            score = budget_map.get(text(destination.get("name")), 0)
        else:
            score = attribute_score(destination, requirement, requested_geography)

        scores.append(clamp(score))

    s_score = season_score(destination, requested_seasons)
    if s_score is not None:
        scores.append(s_score)

    g_score = geography_score(destination, requested_geography)
    if g_score is not None:
        scores.append(g_score)

    # If a prompt contains no measurable preference, give every filtered
    # destination a neutral score instead of returning 0%.
    if not scores:
        return 50.0

    # Geographical/season filters are preferences, not hidden penalties.
    # Only explicitly requested attributes affect the result.
    return clamp(sum(scores) / len(scores))


# ============================================================
# DESCRIPTION
# ============================================================

def create_description(destination):
    environment = str(destination.get("environment") or "").strip()
    geography = str(destination.get("geography") or "").strip()

    if environment:
        return environment[:1].upper() + environment[1:] + "."

    if geography:
        return geography[:1].upper() + geography[1:] + "."

    return "A beautiful lesser-known destination waiting to be explored."


# ============================================================
# RESPONSE OBJECT
# ============================================================

def build_recommendation(destination, score):
    return {
        "name": destination.get("name"),
        "state": destination.get("state"),
        "latitude": destination.get("latitude"),
        "longitude": destination.get("longitude"),
        "budget": destination.get("budget"),
        "nature_score": destination.get("nature_score"),
        "adventure_score": destination.get("adventure_score"),
        "culture_score": destination.get("culture_score"),
        "crowd_score": destination.get("crowd_score"),
        "accessibility_score": destination.get("accessibility_score"),
        "best_season": destination.get("best_season"),
        "tourism_saturation": destination.get("tourism_saturation"),
        "geography": destination.get("geography", ""),
        "architecture": destination.get("architecture", ""),
        "environment": destination.get("environment", ""),
        "temperature": destination.get("temperature", ""),
        "description": create_description(destination),
        "match_score": score,
    }


# ============================================================
# DESTINATION LOADING
# ============================================================

def load_destinations():
    docs = db.collection("destinations").stream()
    destinations = []
    seen = set()

    for doc in docs:
        data = doc.to_dict()
        name = str(data.get("name") or "").strip()

        if not name:
            continue

        key = name.lower()
        if key in seen:
            continue

        seen.add(key)
        destinations.append(data)

    return destinations


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "DesiTrails AI backend is running",
        "version": "10.0",
    }


# ============================================================
# ALL DESTINATIONS
# ============================================================

@app.get("/destinations")
def get_destinations():
    return {"destinations": load_destinations()}


# ============================================================
# RECOMMEND FROM PROMPT
# ============================================================

@app.post("/recommend-from-prompt")
def recommend_from_prompt(user_prompt: UserPrompt):
    parsed = parse_user_prompt(user_prompt.prompt)

    if not parsed.get("travel_related", False):
        return {
            "success": False,
            "message": "Ask relevant questions related to travel",
            "recommendations": [],
            "parsed_preferences": parsed,
        }

    if parsed.get("invalid_location", False):
        return {
            "success": False,
            "message": "Please give only the names of Indian states.",
            "recommendations": [],
            "parsed_preferences": parsed,
        }

    destinations = load_destinations()

    if not destinations:
        return {
            "success": False,
            "message": "No destinations are currently available.",
            "recommendations": [],
            "parsed_preferences": parsed,
        }

    # --------------------------------------------------------
    # STATE FILTER
    # --------------------------------------------------------

    requested_states = {
        text(state) for state in parsed.get("states", [])
    }

    if requested_states:
        filtered = [
            destination for destination in destinations
            if text(destination.get("state")) in requested_states
        ]
    else:
        filtered = destinations

    if not filtered:
        return {
            "success": False,
            "message": "No destinations found for the selected state.",
            "recommendations": [],
            "parsed_preferences": parsed,
        }

    # --------------------------------------------------------
    # BUDGET MAP
    # --------------------------------------------------------

    requirements = parsed.get("requirements", [])

    budget_requirement = None
    if "cheap" in requirements:
        budget_requirement = "cheap"
    elif "expensive" in requirements:
        budget_requirement = "expensive"

    budget_map = (
        budget_scores(filtered, budget_requirement)
        if budget_requirement
        else {}
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    scored = []

    for destination in filtered:
        score = score_destination(
            destination,
            requirements,
            parsed.get("seasons", []),
            parsed.get("geography", []),
            budget_map,
        )
        scored.append((destination, score))

    # Stable tie-breakers:
    # 1. match score
    # 2. higher nature score
    # 3. lower crowd score
    scored.sort(
        key=lambda item: (
            item[1],
            to_number(item[0].get("nature_score"), 0),
            -to_number(item[0].get("crowd_score"), 10),
        ),
        reverse=True,
    )

    top = scored[:3]

    recommendations = [
        build_recommendation(destination, score)
        for destination, score in top
    ]

    return {
        "success": True,
        "message": "Recommendations generated successfully",
        "parsed_preferences": parsed,
        "recommendations": recommendations,
    }
