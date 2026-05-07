"""
WanderSutra AI Engine
FINAL SAFE VERSION
"""

import logging

from pathlib import Path

import pandas as pd

logger = logging.getLogger("WanderSutra.AI")


SEASON_MAP = {

    12: "Winter",
    1: "Winter",
    2: "Winter",

    3: "Summer",
    4: "Summer",
    5: "Summer",

    6: "Monsoon",
    7: "Monsoon",
    8: "Monsoon",
    9: "Monsoon",

    10: "Post Monsoon",
    11: "Post Monsoon",

}


class India360TravelAI:

    def __init__(self, models_dir):

        self.models_dir = Path(models_dir)

    @property
    def is_ready(self):

        return True


    # ─────────────────────────────
    # SAFE HELPERS
    # ─────────────────────────────

    def _safe_float(self, value, default=0.0):

        try:
            return float(value)

        except:
            return default


    def _safe_int(self, value, default=0):

        try:
            return int(value)

        except:
            return default


    # ─────────────────────────────
    # SCORE
    # ─────────────────────────────

    def _calculate_score(self, row):

        weather_score = self._safe_float(

            row.get("weather_score", 7)

        )

        crowd = self._safe_float(

            row.get("crowd_index", 5)

        )

        score = (

            (weather_score * 0.7)

            +

            ((10 - crowd) * 0.3)

        )

        return round(

            max(1, min(score, 10)),

            1

        )


    # ─────────────────────────────
    # TRANSPORT
    # ─────────────────────────────

    def _calculate_transport(self, distance):

        if distance < 300:

            return "Car"

        elif distance < 900:

            return "Train"

        return "Flight"


    # ─────────────────────────────
    # TRAVEL COST
    # ─────────────────────────────

    def _calculate_travel_cost(

        self,

        distance,

        transport

    ):

        if transport == "Car":

            return distance * 5

        elif transport == "Train":

            return distance * 2

        return distance * 6


    # ─────────────────────────────
    # CONFIDENCE
    # ─────────────────────────────

    def _calculate_confidence(

        self,

        score

    ):

        return round(

            min(0.95, max(0.55, score / 10)),

            2

        )


    # ─────────────────────────────
    # AI TEXT
    # ─────────────────────────────

    def _generate_ai_text(

        self,

        score,

        season

    ):

        if score >= 8:

            return f"Excellent destination for {season}. Highly recommended for travel."

        elif score >= 6:

            return f"Good travel conditions expected during {season}."

        return f"Average travel conditions during {season}."


    # ─────────────────────────────
    # MAIN PREDICT
    # ─────────────────────────────

    def predict(

        self,

        source,

        destination,

        df,

        month,

        budget,

        purpose,

        group_type

    ):

        if df is None or df.empty:

            return {

                "error": "Dataset missing"

            }

        destination_clean = (

            str(destination)

            .lower()

            .strip()

        )

        df_local = df.copy()

        df_local["destination_clean"] = (

            df_local["destination"]

            .astype(str)

            .str.lower()

            .str.strip()

        )

        matches = df_local[

            df_local["destination_clean"]

            == destination_clean

        ]

        if matches.empty:

            matches = df_local[

                df_local["destination_clean"]

                .str.contains(

                    destination_clean,

                    na=False

                )

            ]

        if matches.empty:

            return {

                "error": f"{destination} not found"

            }

        if "month" in matches.columns:

            row = matches.iloc[
                (
                    matches["month"] - int(month)
                ).abs().argsort().iloc[0]
            ]

        else:

            row = matches.iloc[0]

        return self._build_response(

            row,

            source,

            destination,

            month,

            budget

        )


    # ─────────────────────────────
    # RESPONSE
    # ─────────────────────────────

    def _build_response(

        self,

        row,

        source,

        destination,

        month,

        budget

    ):

        hotel_price = self._safe_float(

            row.get("hotel_price_avg_inr", 2500)

        )

        food_price = self._safe_float(

            row.get("food_cost_per_day_inr", 800)

        )

        stay_days = self._safe_int(

            row.get("recommended_stay_days", 3)

        )

        distance = self._safe_float(

            row.get("distance_from_delhi_km", 500)

        )

        transport = self._calculate_transport(

            distance

        )

        travel_cost = self._calculate_travel_cost(

            distance,

            transport

        )

        budget_multiplier = {

            "budget": 0.7,
            "mid": 1.0,
            "luxury": 1.8,

        }.get(budget, 1.0)

        hotel_cost = (

            hotel_price

            * stay_days

            * budget_multiplier

        )

        food_cost = (

            food_price

            * stay_days

            * budget_multiplier

        )

        travel_cost = (

            travel_cost

            * budget_multiplier

        )

        total_cost = (

            hotel_cost

            + food_cost

            + travel_cost

        )

        score = self._calculate_score(row)

        confidence = self._calculate_confidence(

            score

        )

        season = SEASON_MAP.get(

            int(month),

            "Unknown"

        )

        return {

            "source": source,

            "destination": destination,

            "month": month,

            "predictions": {

                "estimated_cost_inr":

                    round(total_cost),

                "hotel_cost_inr":

                    round(hotel_cost),

                "food_cost_inr":

                    round(food_cost),

                "travel_cost_inr":

                    round(travel_cost),

                "recommended_stay_days":

                    stay_days,

                "best_transport":

                    transport,

                "travel_time_hours":

                    self._safe_float(
                        row.get(
                            "travel_time_hours",
                            8
                        )
                    ),

                "experience_score":

                    score,

                "crowd_index":

                    self._safe_float(
                        row.get(
                            "crowd_index",
                            5
                        )
                    ),

                "season":

                    season,

                "confidence":

                    confidence,

            },

            "weather": {

                "temperature":

                    self._safe_float(
                        row.get(
                            "avg_temp_c",
                            25
                        )
                    ),

                "humidity":

                    self._safe_float(
                        row.get(
                            "humidity_pct",
                            60
                        )
                    ),

                "rainfall":

                    self._safe_float(
                        row.get(
                            "rainfall_mm",
                            80
                        )
                    ),

            },

            "geography": {

                "altitude_m":

                    self._safe_float(
                        row.get(
                            "altitude_m",
                            300
                        )
                    ),

                "latitude":

                    self._safe_float(
                        row.get(
                            "latitude",
                            20.59
                        )
                    ),

                "longitude":

                    self._safe_float(
                        row.get(
                            "longitude",
                            78.96
                        )
                    ),

            },

            "ai_text":

                self._generate_ai_text(
                    score,
                    season
                ),

        }


# ─────────────────────────────
# GLOBALS
# ─────────────────────────────

_engine = None

_df = None


def get_engine():

    global _engine

    if _engine is None:

        from django.conf import settings

        _engine = India360TravelAI(

            settings.MODELS_DIR

        )

    return _engine


def get_df():

    global _df

    if _df is None:

        from django.conf import settings

        path = settings.DATA_PATH

        if Path(path).exists():

            _df = pd.read_csv(path)

            _df.columns = (

                _df.columns

                .str.lower()

                .str.strip()

            )

    return _df


def list_destinations(df):

    if df is None:

        return []

    return sorted(

        df["destination"]

        .dropna()

        .unique()

        .tolist()

    )