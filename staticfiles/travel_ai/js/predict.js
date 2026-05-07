"use strict";

const form = document.getElementById("predictForm");
const predictBtn = document.getElementById("predictBtn");

form?.addEventListener("submit", async (e) => {
  e.preventDefault();

  if (predictBtn) predictBtn.disabled = true;

  const payload = {
    source: document.getElementById("source").value,
    destination: document.getElementById("destination").value,
    month: Number(document.getElementById("month").value),
    budget: document.getElementById("budget").value,
    purpose: document.getElementById("purpose").value,
    group_type: document.getElementById("group_type").value,
  };

  try {
    const res = await fetch("/api/predict/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    console.log("API:", data);

    if (data.error) {
      alert(data.error);
      return;
    }

    render(data);

  } catch (err) {
    console.error(err);
    alert("Server error");
  } finally {
    if (predictBtn) predictBtn.disabled = false;
  }
});


function render(data) {
  document.getElementById("resultsPanel").style.display = "block";

  document.getElementById("resSource").textContent = data.source;
  document.getElementById("resDestination").textContent = data.destination;

  document.getElementById("kpiCostVal").textContent = "₹" + data.predictions.estimated_cost_inr;
}