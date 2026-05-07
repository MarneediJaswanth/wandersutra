"use strict";

/* =========================================
   WANDERSUTRA UI ENGINE
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    const plannerBtn =
        document.getElementById("startPlanningBtn");

    const plannerSection =
        document.getElementById("plannerSection");


    /* START BUTTON */
    if (plannerBtn && plannerSection) {

        plannerBtn.addEventListener("click", () => {

            plannerSection.classList.add("show-section");

            plannerSection.scrollIntoView({
                behavior: "smooth"
            });

        });

    }

});


console.log("WanderSutra Loaded");