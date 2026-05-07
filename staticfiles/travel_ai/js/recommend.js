"use strict";

const recommendForm = document.getElementById("recommendForm");

const recResults = document.getElementById("recResults");

const recLoading = document.getElementById("recLoading");

const recBtn = document.getElementById("recBtn");


// FORMAT INR
function formatINR(amount) {

    if (!amount && amount !== 0) {
        return "—";
    }

    return "₹" + Number(amount).toLocaleString("en-IN");
}


// TITLE CASE
function titleCase(text) {

    if (!text) return "—";

    return text.replace(/\b\w/g, c => c.toUpperCase());
}


// FORM SUBMIT
if (recommendForm) {

    recommendForm.addEventListener("submit", async function(e) {

        e.preventDefault();

        recLoading.classList.remove("hidden");

        recResults.innerHTML = "";

        recBtn.disabled = true;

        recBtn.innerText = "Loading...";

        try {

            const params = new URLSearchParams({

                month: document.getElementById("rMonth").value,

                budget: document.getElementById("rBudget").value,

                purpose: document.getElementById("rPurpose").value,

                group_type: document.getElementById("rGroup").value,

                top_n: document.getElementById("rTopN").value

            });

            const response = await fetch(

                `/api/recommend/?${params}`

            );

            const data = await response.json();

            recLoading.classList.add("hidden");

            if (!data.results || data.results.length === 0) {

                recResults.innerHTML = `

                    <div class="empty-rec">

                        No destinations found

                    </div>

                `;

                return;
            }

            renderRecommendations(data.results);

        }

        catch (error) {

            console.log(error);

            recLoading.classList.add("hidden");

            recResults.innerHTML = `

                <div class="empty-rec">

                    Unable to load recommendations

                </div>

            `;

        }

        finally {

            recBtn.disabled = false;

            recBtn.innerText = "Find Recommendations";

        }

    });

}


// RENDER RECOMMENDATIONS
function renderRecommendations(results) {

    recResults.innerHTML = "";

    results.forEach(function(item, index) {

        const card = document.createElement("div");

        card.className = "recommend-card";

        card.innerHTML = `

            <div class="recommend-rank">

                #${index + 1}

            </div>

            <div class="recommend-content">

                <h2>

                    ${titleCase(item.destination)}

                </h2>

                <p class="recommend-state">

                    ${titleCase(item.state || "India")}

                </p>

                <div class="recommend-details">

                    <div class="recommend-item">

                        <span>Experience</span>

                        <strong>

                            ${Number(item.experience_score || 0).toFixed(1)}/10

                        </strong>

                    </div>

                    <div class="recommend-item">

                        <span>Crowd</span>

                        <strong>

                            ${Number(item.crowd_index || 0).toFixed(1)}/10

                        </strong>

                    </div>

                    <div class="recommend-item">

                        <span>Temperature</span>

                        <strong>

                            ${item.avg_temp_c || "—"}°C

                        </strong>

                    </div>

                    <div class="recommend-item">

                        <span>Stay</span>

                        <strong>

                            ${item.recommended_stay_days || "—"} Days

                        </strong>

                    </div>

                </div>

            </div>

        `;

        recResults.appendChild(card);

    });

}