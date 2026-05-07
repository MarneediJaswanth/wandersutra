"use strict";

/* =========================================
   WANDERSUTRA MAIN ENGINE
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =========================================
       START BUTTON
    ========================================= */

    const startBtn =
        document.getElementById("startPlanningBtn");

    const plannerSection =
        document.getElementById("plannerSection");

    if (startBtn && plannerSection) {

        startBtn.addEventListener("click", () => {

            plannerSection.style.display = "block";

            plannerSection.classList.remove("hidden-section");

            plannerSection.classList.add("show-section");

            setTimeout(() => {

                plannerSection.scrollIntoView({
                    behavior: "smooth"
                });

            }, 200);

        });

    }


    /* =========================================
       FORM SUBMIT
    ========================================= */

    const predictForm =
        document.getElementById("predictForm");

    if (predictForm) {

        predictForm.addEventListener("submit", async (e) => {

            e.preventDefault();

            const payload = {

                source:
                    document.getElementById("source").value,

                destination:
                    document.getElementById("destination").value,

                month:
                    document.getElementById("month").value,

                budget:
                    document.getElementById("budget").value,

            };

            try {

                const response = await fetch("/api/predict/", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(payload)

                });

                const data = await response.json();

                console.log(data);

                if (!response.ok || data.error) {

                    alert(data.error || "Prediction failed");

                    return;

                }

                renderResults(data);

            }

            catch (error) {

                console.error(error);

                alert("Server error");

            }

        });

    }

});


/* =========================================
   RENDER RESULTS
========================================= */

function renderResults(data) {

    const resultsPanel =
        document.getElementById("resultsPanel");

    resultsPanel.style.display = "block";


    /* ROUTE */

    document.getElementById("route").textContent =

        `${capitalize(data.source)} → ${capitalize(data.destination)}`;


    /* CONFIDENCE */

    document.getElementById("confidence").textContent =

        `${Math.round(
            (data.predictions.confidence || 0.8) * 100
        )}%`;


    /* KPI */

    document.getElementById("cost").textContent =

        `₹${data.predictions.estimated_cost_inr || 0}`;


    document.getElementById("stay").textContent =

        `${data.predictions.recommended_stay_days || 0} Days`;


    document.getElementById("transport").textContent =

        data.predictions.best_transport || "N/A";


    document.getElementById("season").textContent =

        data.predictions.season || "N/A";


    /* WEATHER */

    document.getElementById("temp").textContent =

        `${data.weather.temperature || 0} °C`;


    document.getElementById("humidity").textContent =

        `${data.weather.humidity || 0}%`;


    document.getElementById("rain").textContent =

        `${data.weather.rainfall || 0} mm`;


    /* AI TEXT */

    document.getElementById("aiText").textContent =

        data.ai_text || "AI insights generated successfully.";


    /* MAP */

    renderMap(data);


    /* CHARTS */

    renderCostChart(data);

    renderWeatherChart(data);


    /* SCROLL */

    setTimeout(() => {

        resultsPanel.scrollIntoView({

            behavior: "smooth"

        });

    }, 300);

}


/* =========================================
   MAP
========================================= */

let travelMap = null;

function renderMap(data) {

    const lat =
        data.geography.latitude || 20.5937;

    const lon =
        data.geography.longitude || 78.9629;

    if (travelMap) {

        travelMap.remove();

    }

    travelMap = L.map("map").setView([lat, lon], 6);

    L.tileLayer(

        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

        {

            attribution: "© OpenStreetMap"

        }

    ).addTo(travelMap);

    L.marker([lat, lon])

        .addTo(travelMap)

        .bindPopup(data.destination)

        .openPopup();

}


/* =========================================
   COST CHART
========================================= */

let costChart = null;

function renderCostChart(data) {

    const ctx =
        document.getElementById("costChartCanvas");

    if (costChart) {

        costChart.destroy();

    }

    costChart = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: [

                "Hotel",
                "Food",
                "Travel"

            ],

            datasets: [{

                data: [

                    data.predictions.hotel_cost_inr || 0,

                    data.predictions.food_cost_inr || 0,

                    data.predictions.travel_cost_inr || 0

                ],

                backgroundColor: [

                    "#2563eb",
                    "#7c3aed",
                    "#06b6d4"

                ]

            }]

        }

    });

}


/* =========================================
   WEATHER CHART
========================================= */

let weatherChart = null;

function renderWeatherChart(data) {

    const ctx =
        document.getElementById("weatherChartCanvas");

    if (weatherChart) {

        weatherChart.destroy();

    }

    weatherChart = new Chart(ctx, {

        type: "bar",

        data: {

            labels: [

                "Temperature",
                "Humidity",
                "Rainfall"

            ],

            datasets: [{

                label: "Weather",

                data: [

                    data.weather.temperature || 0,

                    data.weather.humidity || 0,

                    data.weather.rainfall || 0

                ],

                backgroundColor: [

                    "#2563eb",
                    "#7c3aed",
                    "#06b6d4"

                ]

            }]

        }

    });

}


/* =========================================
   HELPER
========================================= */

function capitalize(text) {

    if (!text) return "";

    return text.charAt(0).toUpperCase() +

        text.slice(1);

}