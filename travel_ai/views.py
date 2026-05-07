"""
WanderSutra — AI Travel Planning System
FINAL CLEAN VERSION
"""

import json
import logging

from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .ai_engine import (
    get_engine,
    get_df,
    list_destinations
)

logger = logging.getLogger("WanderSutra.Views")


# ─────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────

MONTH_NAMES = {

    1: "January",
    2: "February",
    3: "March",
    4: "April",

    5: "May",
    6: "June",
    7: "July",
    8: "August",

    9: "September",
    10: "October",
    11: "November",
    12: "December",

}


BUDGET_CHOICES = [

    ("budget", "Budget"),

    ("mid", "Mid Range"),

    ("luxury", "Luxury"),

]


PURPOSE_CHOICES = [

    ("leisure", "Leisure"),

    ("adventure", "Adventure"),

    ("romantic", "Romantic"),

    ("business", "Business"),

]


GROUP_CHOICES = [

    ("solo", "Solo"),

    ("couple", "Couple"),

    ("family", "Family"),

    ("friends", "Friends"),

]


# ─────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────

def index(request):

    df = get_df()

    destinations = []

    if df is not None:

        destinations = list_destinations(df)

    return render(

        request,

        "travel_ai/index.html",

        {

            "destinations": destinations,

            "month_choices": MONTH_NAMES.items(),

            "budget_choices": BUDGET_CHOICES,

            "purpose_choices": PURPOSE_CHOICES,

            "group_choices": GROUP_CHOICES,

        }

    )


# ─────────────────────────────────────
# ABOUT PAGE
# ─────────────────────────────────────

def about(request):

    engine = get_engine()

    return render(

        request,

        "travel_ai/about.html",

        {

            "models_loaded": engine.is_ready

        }

    )


# ─────────────────────────────────────
# HEALTH API
# ─────────────────────────────────────

def api_health(request):

    engine = get_engine()

    df = get_df()

    return JsonResponse({

        "status": "healthy",

        "models_loaded": engine.is_ready,

        "dataset_rows":

            len(df)

            if df is not None

            else 0,

    })


# ─────────────────────────────────────
# DESTINATIONS API
# ─────────────────────────────────────

def api_destinations(request):

    df = get_df()

    return JsonResponse({

        "destinations":

            list_destinations(df)

            if df is not None

            else []

    })


# ─────────────────────────────────────
# MAIN AI PREDICTION API
# ─────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])

def api_predict(request):

    try:

        body = json.loads(request.body)

    except Exception:

        return JsonResponse({

            "error": "Invalid JSON"

        }, status=400)

    source = str(
        body.get("source", "")
    ).strip()

    destination = str(
        body.get("destination", "")
    ).strip()

    try:

        month = int(
            body.get("month", 6)
        )

    except:

        month = 6

    budget = body.get("budget", "mid")

    purpose = body.get("purpose", "leisure")

    group_type = body.get("group_type", "solo")


    # ─────────────────────────────
    # VALIDATION
    # ─────────────────────────────

    if not source:

        return JsonResponse({

            "error": "Source is required"

        }, status=400)

    if not destination:

        return JsonResponse({

            "error": "Destination is required"

        }, status=400)


    # ─────────────────────────────
    # AI ENGINE
    # ─────────────────────────────

    try:

        engine = get_engine()

        df = get_df()

        result = engine.predict(

            source,

            destination,

            df,

            month,

            budget,

            purpose,

            group_type

        )

        if "error" in result:

            return JsonResponse(

                result,

                status=400

            )

        return JsonResponse({

            "source":

                result.get("source"),

            "destination":

                result.get("destination"),

            "month":

                result.get("month"),

            "predictions":

                result.get("predictions", {}),

            "weather":

                result.get("weather", {}),

            "geography":

                result.get("geography", {}),

            "ai_text":

                result.get("ai_text", ""),

        })

    except Exception as e:

        logger.exception(e)

        return JsonResponse({

            "error": "Internal server error"

        }, status=500)